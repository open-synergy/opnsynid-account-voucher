# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class VoucherType(models.Model):
    _name = "account.voucher_type"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Voucher Type"

    name = fields.Char(
        string="Type",
    )
    allowed_journal_ids = fields.One2many(
        string="Allowed Journals",
        comodel_name="account.voucher_type_allowed_journal",
        inverse_name="voucher_type_id",
    )
    check_total = fields.Boolean(
        string="Check Total",
    )
    check_debit_credit = fields.Boolean(
        string="Check Dr/Cr",
    )
    check_partner = fields.Boolean(
        string="Check Partner",
    )
    header_allow_negative = fields.Boolean(
        string="Allow Negative on Header",
    )
    detail_allow_negative = fields.Boolean(
        string="Allow Negative on Detail",
    )
    create_header_item = fields.Boolean(
        string="Create Header Move Line",
    )
    header_type = fields.Selection(
        string="Header Type",
        selection=[
            ("dr", "Debit"),
            ("cr", "Credit"),
        ],
    )
    python_code = fields.Text(
        string="Domain Expression",
        help="The result of executing the expresion must be a domain.",
        default="# Available locals:\n#  - rec: current record\n"
        "# - env: Environment",
    )

    def action_execute(self):
        return True
