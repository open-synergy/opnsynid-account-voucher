# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class WizardImportMoveLine(models.TransientModel):
    _name = "account.wizard_import_move_line"
    _description = "Wizard Import Move Line"

    @api.model
    def default_get(self, fields):
        _super = super(WizardImportMoveLine, self)
        res = _super.default_get(fields)
        active_model = self.env.context.get("active_model", False)
        active_id = self.env.context.get("active_id", False)
        import_type = self.env.context.get("import_type", False)

        voucher = self.env[active_model].browse([active_id])[0]

        res["partner_id"] = voucher.partner_id and voucher.partner_id.id \
            or False
        res["import_type"] = import_type

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
        "partner_id", "import_type",
    )
    def onchange_move_line_ids(self):
        result = {
            "domain": {
                "move_line_ids": [("id", "=", 0)],
            }
        }
        self.move_line_ids = False
        if self.partner_id and self.import_type:
            criteria = [
                ("partner_id", "=", self.partner_id.id),
                ("account_id.reconcile", "=", True),
                ("reconcile_id", "=", False)
            ]
            if self.import_type == "dr":
                criteria.append(("debit", ">", 0))
            else:
                criteria.append(("credit", ">", 0))
            result["domain"]["move_line_ids"] = criteria
        return result

    @api.multi
    def action_import_move_line(self):
        self.ensure_one()
        active_model = self.env.context.get("active_model", False)
        active_id = self.env.context.get("active_id", False)
        voucher = self.env[active_model].browse([active_id])[0]
        lines = []

        for move in self.move_line_ids:
            amount = move.amount_residual / voucher.exchange_rate
            line_type = self.import_type == "dr" and "cr" or "dr"
            res = (0, 0, {
                "name": move.name,
                "partner_id": move.partner_id and move.partner_id.id or False,
                "move_line_id": move.id,
                "account_id": move.account_id.id,
                "amount": amount,
                "type": line_type,
            })
            lines.append(res)
        voucher.write({
            "line_ids": lines,
        })
