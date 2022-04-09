# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class MixinBankVoucher(models.AbstractModel):
    _name = "mixin.bank_voucher"
    _inherit = "mixin.account.voucher"
    _description = "Bank Voucher"
