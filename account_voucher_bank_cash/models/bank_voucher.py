# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class BankVoucher(models.AbstractModel):
    _name = "account.bank_voucher"
    _inherit = "account.voucher_common"
    _description = "Bank Voucher"

    payment_mode_id = fields.Many2one(
        string="Payment Mode",
        comodel_name="payment.mode",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.onchange("journal_id")
    def onchange_payment_mode_id(self):
        result = {
            "domain": {
                "payment_mode_id": [
                    ("id", "=", 0),
                ]
            },
        }
        if self.journal_id:
            result["domain"]["payment_mode_id"] = \
                [("journal", "=", self.journal_id.id)]

            if self.payment_mode_id:
                if self.payment_mode_id.journal != \
                        self.journal_id:
                    self.payment_mode_id = False
            else:
                self.payment_mode_id = False
        return result
