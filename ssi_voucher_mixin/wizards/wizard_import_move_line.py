# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).
# pylint: disable=W0622
import logging

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)


class WizardImportMoveLine(models.TransientModel):
    _name = "account.wizard_import_move_line"
    _description = "Wizard Import Move Line"

    @api.model
    def default_get(self, fields):
        _super = super(WizardImportMoveLine, self)
        res = _super.default_get(fields)
        voucher = self._get_object()

        res["partner_id"] = voucher.partner_id and voucher.partner_id.id or False
        res["import_type"] = self.env.context.get("import_type", False)

        return res

    move_line_ids = fields.Many2many(
        string="Move Lines",
        comodel_name="account.move.line",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        required=True,
    )
    import_type = fields.Selection(
        string="Type",
        selection=[
            ("dr", "Dr"),
            ("cr", "Cr"),
        ],
        required=True,
    )

    @api.onchange(
        "partner_id",
        "import_type",
    )
    def onchange_move_line_ids(self):
        criteria = []
        result = {
            "domain": {
                "move_line_ids": [("id", "=", 0)],
            }
        }
        self.move_line_ids = False

        if self.partner_id and self.import_type:
            commercial_partner_id = self.partner_id.commercial_partner_id.id

            criteria = [
                ("account_id.reconcile", "=", True),
                ("reconciled", "=", False),
                ("partner_id", "=", commercial_partner_id),
            ]
            if self.import_type == "dr":
                criteria.append(("debit", ">", 0))
            else:
                criteria.append(("credit", ">", 0))
        voucher = self._get_object()
        domain_type = self.get_domain_expression(voucher.type_id.python_code)
        if domain_type:
            if isinstance(domain_type, list):
                if len(domain_type) > 1:
                    for document in domain_type:
                        criteria.append(document)
                else:
                    criteria.append(domain_type[0])

        allowed_journal_ids = voucher.type_id.allowed_journal_ids
        for allowed_journal in allowed_journal_ids:

            domain_type_allowed_journal = self.get_domain_expression(
                allowed_journal.python_code
            )
            if domain_type_allowed_journal:
                if isinstance(domain_type_allowed_journal, list):
                    if len(domain_type) > 1:
                        for document in domain_type_allowed_journal:
                            criteria.append(document)
                    else:
                        criteria.append(domain_type_allowed_journal[0])
        result["domain"]["move_line_ids"] = criteria
        return result

    def action_import_move_line(self):
        voucher = self._get_object()
        lines = []

        for move in self.move_line_ids:
            # raise UserError(_("%s")%(move.amount_residual))
            amount = move.amount_residual / voucher.exchange_rate
            line_type = self.import_type == "dr" and "cr" or "dr"
            res = (
                0,
                0,
                {
                    "name": move.name or "-",
                    "partner_id": move.partner_id and move.partner_id.id or False,
                    "move_line_id": move.id,
                    "account_id": move.account_id.id,
                    "amount": abs(amount),
                    "type": line_type,
                },
            )
            lines.append(res)
        voucher.write(
            {
                "line_ids": lines,
            }
        )

    def _get_object(self):
        active_id = self.env.context.get("active_id", False)
        active_model = self.env.context.get("active_model", "")
        object = self.env[active_model].browse([active_id])[0]
        return object

    def _get_localdict(self):
        return {
            "env": self.env,
            "rec": self._get_object(),
        }

    def get_domain_expression(self, python_condition):
        result = []
        localdict = self._get_localdict()
        try:
            safe_eval(python_condition, localdict, mode="exec", nocopy=True)
            result = localdict["result"]
        except Exception as err:
            _logger.info("Error: {}".format(err))

        return result
