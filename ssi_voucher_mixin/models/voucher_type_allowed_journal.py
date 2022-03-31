# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class VoucherTypeAllowedJournal(models.Model):
    _name = "account.voucher_type_allowed_journal"
    _description = "Voucher Type Allowed Journal"

    voucher_type_id = fields.Many2one(
        string="Voucher Type",
        comodel_name="account.voucher_type",
        required=True,
    )
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        required=True,
    )
    python_code = fields.Text(
        string="Domain Expression",
        help="The result of executing the expresion must be a domain.",
        default="# Available locals:\n#  - rec: current record\n"
        "# - env: Environment",
    )

    @api.constrains(
        "voucher_type_id",
        "journal_id",
    )
    def _check_journal_id(self):
        if self.journal_id and self.voucher_type_id:
            strWarning = _("No duplicate journal")
            check_journal = self.search(
                [
                    ("voucher_type_id", "=", self.voucher_type_id.id),
                    ("journal_id", "=", self.journal_id.id),
                ]
            )
            if len(check_journal) > 1:
                raise UserError(strWarning)
