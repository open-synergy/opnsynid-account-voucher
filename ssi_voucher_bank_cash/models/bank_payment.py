# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class BankPayment(models.Model):
    _name = "account.bank_payment"
    _inherit = "mixin.bank_voucher"
    _description = "Bank Payment"

    @api.model
    def _default_type_id(self):
        return self.env.ref("ssi_voucher_bank_cash.voucher_type_bank_payment").id

    type_id = fields.Many2one(
        default=lambda self: self._default_type_id(),
    )
    company_currency_id = fields.Many2one(
        string="Company Currency",
        comodel_name="res.currency",
        related="company_id.currency_id",
        store=True,
    )

    line_ids = fields.One2many(
        comodel_name="account.bank_payment_line",
    )
    line_dr_ids = fields.One2many(
        comodel_name="account.bank_payment_line",
    )
    line_cr_ids = fields.One2many(
        comodel_name="account.bank_payment_line",
    )


class BankPaymentLine(models.Model):
    _name = "account.bank_payment_line"
    _inherit = "mixin.account.voucher.line"
    _description = "Bank Payment Line"

    voucher_id = fields.Many2one(
        comodel_name="account.bank_payment",
    )
    tax_ids = fields.One2many(
        comodel_name="account.bank_payment_line_tax",
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        related="voucher_id.currency_id",
        store=True,
    )
    company_currency_id = fields.Many2one(
        comodel_name="res.currency",
        related="voucher_id.company_currency_id",
        store=True,
    )


class BankPaymentLineTax(models.Model):
    _name = "account.bank_payment_line_tax"
    _inherit = "mixin.account.voucher.line.tax"
    _description = "Bank Payment Line Tax"

    voucher_line_id = fields.Many2one(
        comodel_name="account.bank_payment_line",
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        related="voucher_line_id.currency_id",
        store=True,
    )
    company_currency_id = fields.Many2one(
        comodel_name="res.currency",
        related="voucher_line_id.company_currency_id",
        store=True,
    )
