# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError


class BankPayment(models.Model):
    _name = "account.bank_payment"
    _inherit = "account.bank_payment"
    _description = "Bank Payment"

    payment_order_id = fields.Many2one(
        string="# Payment Order",
        comodel_name="payment.order",
        readonly=True,
        ondelete="restrict",
    )

    @api.constrains(
        "state"
    )
    def _check_payment_order(self):
        str_error = _("Finish payment order first")
        for document in self:
            if document.state == "post" and \
                    document.payment_order_id and \
                    document.payment_order_id.state != "done":
                raise UserError(str_error)

    @api.multi
    def _prepare_approve_data(self):
        self.ensure_one()
        _super = super(BankPayment, self)
        data = _super._prepare_approve_data()
        payment_order_id = self._create_payment_order()
        data.update({
            "payment_order_id": payment_order_id,
        })

        return data

    @api.multi
    def _create_payment_order(self):
        result = False
        if self.payment_mode_id:
            obj_payment = self.env["payment.order"]
            result = obj_payment.create(self._prepare_payment_order())
        return result and result.id or False

    @api.multi
    def _prepare_payment_order(self):
        self.ensure_one()
        return {
            "date_scheduled": self.date_voucher,
            "mode": self.payment_mode_id.id,
            "user_id": self.env.user.id,
            "date_prefered": "fixed",
            "line_ids": self._prepare_payment_order_line()
        }

    @api.multi
    def _prepare_payment_order_line(self):
        self.ensure_one()
        result = []
        for line in self.line_ids:
            result.append(line._prepare_payment_order_line())
        return result

    @api.multi
    def _prepare_cancel_data(self):
        _super = super(BankPayment, self)
        data = _super._prepare_cancel_data()
        payment_order = self.payment_order_id
        self.write({
            "payment_order_id": False,
        })
        if payment_order:
            payment_order.unlink()
        return data
