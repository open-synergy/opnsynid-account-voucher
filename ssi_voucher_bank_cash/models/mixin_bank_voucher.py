# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class MixinBankVoucher(models.AbstractModel):
    _name = "mixin.bank_voucher"
    _inherit = "mixin.account.voucher"
    _description = "Bank Voucher"

    payment_mode_id = fields.Many2one(
        string="Payment Mode",
        comodel_name="payment.acquirer",
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
            result["domain"]["payment_mode_id"] = [
                ("journal_id", "=", self.journal_id.id)
            ]

            if self.payment_mode_id:
                if self.payment_mode_id.journal != self.journal_id:
                    self.payment_mode_id = False
            else:
                self.payment_mode_id = False
        return result
