# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import api, fields, models


class ChequeReceipt(models.Model):
    _name = "account.cheque_receipt"
    _inherit = "mixin.cheque_voucher"
    _description = "Cheque Receipt"

    @api.model
    def _default_type_id(self):
        return self.env.ref("ssi_voucher_cheque.voucher_type_cheque_receipt").id

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
        comodel_name="account.cheque_receipt_line",
    )
    line_dr_ids = fields.One2many(
        comodel_name="account.cheque_receipt_line",
    )
    line_cr_ids = fields.One2many(
        comodel_name="account.cheque_receipt_line",
    )


class ChequeReceiptLine(models.Model):
    _name = "account.cheque_receipt_line"
    _inherit = "mixin.account.voucher.line"
    _description = "Cheque Receipt Line"

    voucher_id = fields.Many2one(
        comodel_name="account.cheque_receipt",
    )
    tax_ids = fields.One2many(
        comodel_name="account.cheque_receipt_line_tax",
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


class ChequeReceiptLineTax(models.Model):
    _name = "account.cheque_receipt_line_tax"
    _inherit = "mixin.account.voucher.line.tax"
    _description = "Cheque Receipt Line Tax"

    voucher_line_id = fields.Many2one(
        comodel_name="account.cheque_receipt_line",
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
