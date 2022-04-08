# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class SaleRefundSettlement(models.Model):
    _name = "account.sale_refund_settlement"
    _inherit = "mixin.account.voucher"
    _description = "Sale Refund Settlement"

    @api.model
    def _default_type_id(self):
        return self.env.ref(
            "ssi_voucher_refund_settlement." "voucher_type_sale_refund_settlement"
        ).id

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
        comodel_name="account.sale_refund_settlement_line",
    )
    line_dr_ids = fields.One2many(
        comodel_name="account.sale_refund_settlement_line",
    )
    line_cr_ids = fields.One2many(
        comodel_name="account.sale_refund_settlement_line",
    )


class SaleRefundSettlementLine(models.Model):
    _name = "account.sale_refund_settlement_line"
    _inherit = "mixin.account.voucher.line"
    _description = "Sale Refund Settlement Line"

    voucher_id = fields.Many2one(
        comodel_name="account.sale_refund_settlement",
    )
    tax_ids = fields.One2many(
        comodel_name="account.sale_refund_settlement_line_tax",
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


class SaleRefundSettlementLineTax(models.Model):
    _name = "account.sale_refund_settlement_line_tax"
    _inherit = "mixin.account.voucher.line.tax"
    _description = "Sale Refund Settlement Line Tax"

    voucher_line_id = fields.Many2one(
        comodel_name="account.sale_refund_settlement_line",
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
