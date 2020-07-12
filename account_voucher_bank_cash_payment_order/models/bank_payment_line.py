# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api


class BankPaymentLine(models.Model):
    _name = "account.bank_payment_line"
    _inherit = "account.bank_payment_line"
    _description = "Bank Payment Line"

    @api.multi
    def _prepare_payment_order_line(self):
        self.ensure_one()
        move_line_id = self.move_line_id and self.move_line_id.id or False
        partner_id = self.partner_id and self.partner_id or False
        bank_id = self.partner_id.bank_ids and \
            self.partner_id.bank_ids[0].id or False
        result = [0, 0, {
            "communication": self.name,
            "amount_currency": self.amount_company_currency_move_date,
            "company_currency": self.amount_before_tax,
            "currency": self.voucher_id.currency_id.id,
            "bank_id": bank_id,
            "partner_id": partner_id,
            "move_line_id": move_line_id,
        }]
        return result
