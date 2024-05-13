# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MixinAccountVoucherLineSummary(models.AbstractModel):
    _name = "mixin.account.voucher.line.summary"
    _description = "Abstract Class for Account Voucher Line Summary"
    _auto = False

    voucher_id = fields.Many2one(
        string="Voucher",
        comodel_name="mixin.account.voucher",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
    )
    amount_before_tax = fields.Monetary(
        string="Amount Before Tax",
        currency_field="currency_id",
    )
    amount_tax = fields.Monetary(
        string="Amount Tax",
        currency_field="currency_id",
    )
    amount_after_tax = fields.Monetary(
        string="Amount After Tax",
        currency_field="currency_id",
    )
