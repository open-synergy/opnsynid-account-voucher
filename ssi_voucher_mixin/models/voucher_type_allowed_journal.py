# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

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
    sequence_id = fields.Many2one(
        string="Sequence",
        comodel_name="ir.sequence",
    )
    allowed_confirm_group_ids = fields.Many2many(
        string="Allow to Confirm",
        comodel_name="res.groups",
        relation="rel_vtype_journal_confirm_group",
        column1="vtype_journal_id",
        column2="group_id",
    )
    allowed_restart_approval_group_ids = fields.Many2many(
        string="Allow To Restart Approval",
        comodel_name="res.groups",
        relation="rel_vtype_journal_restart_approval_group",
        column1="vtype_journal_id",
        column2="group_id",
    )
    allowed_proforma_group_ids = fields.Many2many(
        string="Allow to Proforma",
        comodel_name="res.groups",
        relation="rel_vtype_journal_proforma_group",
        column1="vtype_journal_id",
        column2="group_id",
    )
    allowed_post_group_ids = fields.Many2many(
        string="Allow to Post",
        comodel_name="res.groups",
        relation="rel_vtype_journal_post_group",
        column1="vtype_journal_id",
        column2="group_id",
    )
    allowed_cancel_group_ids = fields.Many2many(
        string="Allow to Cancel",
        comodel_name="res.groups",
        relation="rel_vtype_journal_cancel_group",
        column1="vtype_journal_id",
        column2="group_id",
    )
    allowed_approve_group_ids = fields.Many2many(
        string="Allow to Approve",
        comodel_name="res.groups",
        relation="rel_vtype_journal_approve_group",
        column1="vtype_journal_id",
        column2="group_id",
    )
    allowed_reject_group_ids = fields.Many2many(
        string="Allow to Reject",
        comodel_name="res.groups",
        relation="rel_vtype_journal_reject_group",
        column1="vtype_journal_id",
        column2="group_id",
    )
    allowed_restart_group_ids = fields.Many2many(
        string="Allow to Restart",
        comodel_name="res.groups",
        relation="rel_vtype_journal_restart_group",
        column1="vtype_journal_id",
        column2="group_id",
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
