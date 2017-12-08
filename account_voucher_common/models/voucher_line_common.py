# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError


class VoucherLineCommon(models.AbstractModel):
    _name = "account.voucher_line_common"
    _description = "Abstract Class for Voucher Line"

    @api.multi
    @api.depends(
        "amount", "move_line_id",
        "tax_ids", "tax_ids.tax_amount",
        )
    def _compute_amount(self):
        for line in self:
            amount_company_currency_move_date = \
                amount_diff_in_company_currency = \
                amount_company_currency_voucher_date = \
                amount_before_tax = amount_tax = \
                amount_after_tax = \
                0.0
            voucher = line.voucher_id
            move_line = line.move_line_id

            voucher_rate = voucher.exchange_rate
            move_date = move_line and move_line.date or \
                voucher.date_voucher

            amount_before_tax = amount_after_tax = line.amount

            for tax in line.tax_ids:
                amount_tax += tax.tax_amount
                if tax.tax_id.price_include:
                    amount_before_tax -= tax.tax_amount
                elif not tax.tax_id.price_include:
                    amount_after_tax += tax.tax_amount

            amount_company_currency_voucher_date = amount_before_tax * \
                voucher_rate
            amount_company_currency_move_date = line.currency_id.\
                with_context(date=move_date).compute(
                    amount_before_tax, line.company_currency_id)

            amount_diff_in_company_currency = \
                amount_company_currency_voucher_date - \
                amount_company_currency_move_date

            line.amount_diff_in_company_currency = \
                amount_diff_in_company_currency
            line.amount_company_currency_voucher_date = \
                amount_company_currency_voucher_date
            line.amount_company_currency_move_date = \
                amount_company_currency_move_date
            line.amount_before_tax = amount_before_tax
            line.amount_tax = amount_tax
            line.amount_after_tax = amount_after_tax

    name = fields.Char(
        string="Description",
        required=True,
    )
    voucher_id = fields.Many2one(
        string="Voucher",
        comodel_name="account.voucher_common",
        required=True,
        ondelete="cascade",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
        required=True,
        domain=[("type", "not in", ["view", "consolidation", "closed"])],
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
        domain=[("type", "!=", "view")],
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
    )
    type = fields.Selection(
        string="Type",
        selection=[
            ("dr", "Dr"),
            ("cr", "Cr"),
        ],
        required=True,
    )
    move_line_id = fields.Many2one(
        string="Move Line",
        comodel_name="account.move.line",
        copy=False,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
    )
    company_currency_id = fields.Many2one(
        string="Company Currency",
        comodel_name="res.currency",
    )
    amount = fields.Float(
        string="Amount",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    product_uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
    )
    product_qty = fields.Float(
        string="Qty",
    )
    product_unit_price = fields.Float(
        string="Unit Price",
    )
    amount_diff_in_company_currency = fields.Float(
        string="Diff Amount In Company Currency",
        compute="_compute_amount",
        store=True,
    )
    amount_company_currency_move_date = fields.Float(
        string="Amount In Company Currency At Move Date",
        compute="_compute_amount",
        store=True,
    )
    amount_company_currency_voucher_date = fields.Float(
        string="Amount In Company Currency At Voucher Date",
        compute="_compute_amount",
        store=True,
    )
    tax_ids = fields.One2many(
        string="Taxes",
        comodel_name="account.voucher_line_tax_common",
        inverse_name="voucher_line_id",
    )
    amount_before_tax = fields.Float(
        string="Amount Before Tax",
        compute="_compute_amount",
        store=True,
    )
    amount_after_tax = fields.Float(
        string="Amount After Tax",
        compute="_compute_amount",
        store=True,
    )
    amount_tax = fields.Float(
        string="Amount Tax",
        compute="_compute_amount",
        store=True,
    )

    @api.multi
    def _get_debit_credit(self):
        self.ensure_one()
        debit = credit = 0.0
        if self.type == "dr":
            debit = self.amount_company_currency_move_date
        else:
            credit = self.amount_company_currency_move_date
        return (debit, credit)

    @api.multi
    def _get_currency_exchange_information(self):
        self.ensure_one()
        debit = credit = 0.0
        amount = self.amount_diff_in_company_currency
        company = self.env.user.company_id
        if amount < 0:
            credit = abs(amount)
            account_id = company.income_currency_exchange_account_id and \
                company.income_currency_exchange_account_id.id or False
        else:
            debit = abs(amount)
            account_id = company.expense_currency_exchange_account_id and \
                company.expense_currency_exchange_account_id.id or False
        return (debit, credit, account_id)

    @api.multi
    def _get_amount_currency(self):
        self.ensure_one()
        result = 0.0
        if self.type == "dr":
            sign = 1.0
        else:
            sign = -1.0
        company_currency = self.company_currency_id
        if self.move_line_id:
            ml = self.move_line_id
            if ml.currency_id and ml.currency_id != company_currency:
                result = sign * self.amount_before_tax
        else:
            if self.currency_id != company_currency:
                result = sign * self.amount_before_tax
        return result

    @api.multi
    def _create_aml(self):
        self.ensure_one()
        obj_move_line = self.env["account.move.line"]
        move = obj_move_line.create(
            self._prepare_move_line())
        if self.amount_diff_in_company_currency > 0:
            obj_move_line.create(
                self._prepare_exchange_move_line())
        for tax in self.tax_ids:
            obj_move_line.create(
                tax._prepare_move_line())
        if self.move_line_id:
            pair = move + self.move_line_id
            pair.reconcile_partial()

    @api.multi
    def _prepare_move_line(self):
        self.ensure_one()
        debit, credit = self._get_debit_credit()
        voucher = self.voucher_id
        partner_id = self.partner_id and \
            self.partner_id.commercial_partner_id.id or \
            False
        data = {
            "name": self.name,
            "debit": debit,
            "credit": credit,
            "account_id": self.account_id.id,
            "analytic_account_id": self.analytic_account_id and
            self.analytic_account_id.id or False,
            "amount_currency": self._get_amount_currency(),
            "currency_id": self._get_line_currency(),
            "partner_id": partner_id,
            "move_id": voucher.move_id.id,
        }
        return data

    @api.multi
    def _prepare_exchange_move_line(self):
        self.ensure_one()
        debit, credit, account_id = self._get_currency_exchange_information()
        voucher = self.voucher_id
        name = _("Currency exchange for ") + self.name
        partner_id = self.partner_id and \
            self.partner_id.commercial_partner_id.id or \
            False
        data = {
            "name": name,
            "debit": debit,
            "credit": credit,
            "account_id": account_id,
            "analytic_account_id": self.analytic_account_id and
            self.analytic_account_id.id or False,
            "amount_currency": 0.0,
            "currency_id": self._get_line_currency(),
            "partner_id": partner_id,
            "move_id": voucher.move_id.id,
        }
        return data

    @api.onchange("partner_id", "type")
    def onchange_move_line_id(self):

        result = {
            "domain": {
                "move_line_id": [
                    ("reconcile_id", "=", False),
                    ("account_id.reconcile", "=", True),
                ]
            }
        }
        if self.type == "dr":
            result["domain"]["move_line_id"].append(
                ("credit", ">", 0))
        else:
            result["domain"]["move_line_id"].append(
                ("debit", ">", 0))

        if self.partner_id:
            if self.move_line_id:
                result["domain"]["move_line_id"].append(
                    ("partner_id", "=", self.partner_id.id))
                if self.move_line_id.partner_id != self.partner_id:
                    self.move_line_id = False
            else:
                result["domain"]["move_line_id"].append(
                    ("partner_id", "=", self.partner_id.id))
        else:
            self.move_line_id = False
            result["domain"]["move_line_id"].append(
                ("partner_id", "=", False))
        return result

    @api.onchange("move_line_id")
    def onchange_account(self):
        self.account_id = False
        if self.move_line_id:
            self.account_id = self.move_line_id.account_id.id

    @api.onchange("move_line_id")
    def onchange_name(self):
        self.name = "/"
        if self.move_line_id:
            self.name = self.move_line_id.name

    @api.constrains("amount", "voucher_id")
    def _check_negative_value(self):
        str_error = _("Detail value has to be greater than 0")
        if not self.voucher_id.type_id.detail_allow_negative and \
                self.amount < 0:
            raise UserError(str_error)

    @api.multi
    def _get_line_currency(self):
        self.ensure_one()
        result = False
        company_currency = self.company_currency_id
        if self.currency_id != company_currency:
            result = self.currency_id.id
        return result
