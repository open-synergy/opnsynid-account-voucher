# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError


class VoucherType(models.Model):
    _name = "account.voucher_type"
    _description = "Voucher Type"

    name = fields.Char(
        string="Voucher Type",
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
    allowed_restart_validation_group_ids = fields.Many2many(
        string="Allow To Restart Validation",
        comodel_name="res.groups",
        relation="rel_vtype_journal_restart_validation_group",
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
    allowed_restart_group_ids = fields.Many2many(
        string="Allow to Restart",
        comodel_name="res.groups",
        relation="rel_vtype_journal_restart_group",
        column1="vtype_journal_id",
        column2="group_id",
    )

    @api.constrains(
        "voucher_type_id",
        "journal_id",
    )
    def _check_journal_id(self):
        if self.journal_id and self.voucher_type_id:
            strWarning = _("No duplicate journal")
            check_journal =\
                self.search([
                    ("voucher_type_id", "=", self.voucher_type_id.id),
                    ("journal_id", "=", self.journal_id.id)
                ])
            if len(check_journal) > 1:
                raise UserError(strWarning)
