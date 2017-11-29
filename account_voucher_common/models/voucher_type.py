# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


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
