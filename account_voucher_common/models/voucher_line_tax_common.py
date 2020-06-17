# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class VoucherLineTaxCommon(models.AbstractModel):
    _name = "account.voucher_line_tax_common"
    _description = "Abstract Class for Voucher Line Tax"

    @api.multi
    @api.depends(
        "tax_id", "base_amount_computation_method",
        "manual_base_amount", "tax_amount_computation_method",
        "manual_tax_amount",
    )
    def _compute_amount(self):
        for tax in self:
            base_amount = tax_amount = tax_amount_in_company_currency = 0.0
            vline = tax.voucher_line_id
            voucher = vline.voucher_id
            if tax.base_amount_computation_method == "system":
                base_amount = vline.amount
            else:
                base_amount = tax.manual_base_amount

            if tax.tax_amount_computation_method == "system":
                if tax.tax_id:
                    tax_compute = tax.tax_id.compute_all(
                        base_amount, 1)
                    tax_amount = tax_compute["total_included"] - \
                        tax_compute["total"]
            else:
                tax_amount = tax.manual_tax_amount

            tax_amount_in_company_currency = voucher.exchange_rate * tax_amount

            tax.base_amount = base_amount
            tax.tax_amount = tax_amount
            tax.tax_amount_in_company_currency = tax_amount_in_company_currency

    name = fields.Char(
        string="Description",
        required=True,
    )
    voucher_line_id = fields.Many2one(
        string="Voucher Line",
        comodel_name="account.voucher_line_common",
        required=True,
        ondelete="cascade",
    )
    tax_id = fields.Many2one(
        string="Tax",
        comodel_name="account.tax",
        required=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
    )
    company_currency_id = fields.Many2one(
        string="Company Currency",
        comodel_name="res.currency",
    )
    base_amount_computation_method = fields.Selection(
        string="Base Amount Computation Method",
        selection=[
            ("system", "System"),
            ("manual", "Manual"),
        ],
        required=True,
        default="system",
    )
    manual_base_amount = fields.Float(
        string="Base Amount",
    )
    base_amount = fields.Float(
        string="Base Amount",
        compute="_compute_amount",
        store=True,
    )
    tax_amount_computation_method = fields.Selection(
        string="Tax Amount Computation Method",
        selection=[
            ("system", "System"),
            ("manual", "Manual"),
        ],
        required=True,
        default="system",
    )
    manual_tax_amount = fields.Float(
        string="Tax Amount Amount",
    )
    tax_amount = fields.Float(
        string="Tax Amount",
        compute="_compute_amount",
        store=True,
    )
    tax_amount_in_company_currency = fields.Float(
        string="Tax Amount in Company Currency",
        compute="_compute_amount",
        store=True,
    )

    @api.onchange("tax_id")
    def onchange_name(self):
        self.name = "/"
        if self.tax_id:
            self.name = self.tax_id.name

    @api.multi
    def _prepare_move_line(self):
        self.ensure_one()
        debit, credit = self._get_debit_credit()
        vline = self.voucher_line_id
        partner_id = vline.partner_id and \
            vline.partner_id.commercial_partner_id.id or \
            False
        name = self.name + " for " + vline.name
        data = {
            "name": name,
            "debit": debit,
            "credit": credit,
            "account_id": self._get_account().id,
            "analytic_account_id": vline.analytic_account_id and
            vline.analytic_account_id.id or False,
            "amount_currency": self._get_amount_currency(),
            "currency_id": vline._get_line_currency(),
            "partner_id": partner_id,
            "move_id": vline.voucher_id.move_id.id,
            "tax_amount": self.tax_amount_in_company_currency,
            "tax_code_id": self.tax_id.tax_code_id and
            self.tax_id.tax_code_id.id or False,
        }
        return data

    @api.multi
    def _get_account(self):
        self.ensure_one()
        vline = self.voucher_line_id
        result = vline.account_id
        if self.tax_id.account_collected_id:
            result = self.tax_id.account_collected_id
        return result

    @api.multi
    def _get_debit_credit(self):
        self.ensure_one()
        debit = credit = 0.0
        vline = self.voucher_line_id
        amount = self.tax_amount_in_company_currency
        if vline.type == "dr":
            if amount > 0:
                debit = amount
            else:
                credit = amount
        else:
            if amount > 0:
                credit = amount
            else:
                debit = amount
        return (debit, credit)

    @api.multi
    def _get_amount_currency(self):
        self.ensure_one()
        result = 0.0
        vline = self.voucher_line_id
        if vline.type == "dr":
            sign = 1.0
        else:
            sign = -1.0
        sign = sign * (self.tax_id.price_include and 1.0 * -1.0)
        company_currency = vline.company_currency_id
        if vline.currency_id != company_currency:
            result = sign * self.tax_amount
        return result
