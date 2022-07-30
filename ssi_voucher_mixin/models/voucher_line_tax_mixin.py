# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import api, fields, models


class MixinAccountVoucherLineTax(models.AbstractModel):
    _name = "mixin.account.voucher.line.tax"
    _description = "Abstract Class for Voucher Line Tax"

    @api.depends(
        "tax_id",
        "base_amount_computation_method",
        "manual_base_amount",
        "tax_amount_computation_method",
        "manual_tax_amount",
    )
    def _compute_amount(self):
        for tax in self:
            base_amount = tax_amount = tax_amount_in_company_currency = 0.0
            vline = tax.voucher_line_id
            voucher = vline.voucher_id
            taxes = False

            if tax.base_amount_computation_method == "manual":
                base_amount = tax.manual_base_amount

            if tax.tax_amount_computation_method == "manual":
                tax_amount = tax.manual_tax_amount

            if tax.tax_id:
                taxes = tax.tax_id.compute_all(
                    vline.amount, vline.currency_id, 1.0, product=False, partner=False
                )

            if tax.base_amount_computation_method == "system" and taxes:
                base_amount = taxes["total_excluded"]

            if tax.tax_amount_computation_method == "system" and taxes:
                tax_amount = taxes["total_included"] - taxes["total_excluded"]

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
        comodel_name="mixin.account.voucher.line",
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

    def _prepare_move_line(self):
        self.ensure_one()
        debit, credit = self._get_debit_credit()
        vline = self.voucher_line_id
        partner_id = (
            vline.partner_id and vline.partner_id.commercial_partner_id.id or False
        )
        name = self.name + " for " + vline.name
        data = {
            "name": name,
            "debit": debit,
            "credit": credit,
            "account_id": self._get_account_id(),
            "analytic_account_id": vline.analytic_account_id
            and vline.analytic_account_id.id
            or False,
            "amount_currency": self._get_amount_currency(),
            "currency_id": vline._get_line_currency(),
            "partner_id": partner_id,
            "move_id": vline.voucher_id.move_id.id,
        }
        return data

    def _get_account_id(self):
        self.ensure_one()
        vline = self.voucher_line_id
        result = vline.account_id.id
        if self.tax_id:
            taxes = self.tax_id.compute_all(
                vline.amount, vline.currency_id, 1.0, product=False, partner=False
            )
            result = taxes["taxes"][0]["account_id"]
        return result

    def _get_debit_credit(self):
        self.ensure_one()
        debit = credit = 0.0
        vline = self.voucher_line_id
        amount = abs(self.tax_amount_in_company_currency)
        if vline.type == "dr":
            if self.tax_amount_in_company_currency > 0:
                debit = amount
            else:
                credit = amount
        else:
            if self.tax_amount_in_company_currency > 0:
                credit = amount
            else:
                debit = amount
        return (debit, credit)

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
