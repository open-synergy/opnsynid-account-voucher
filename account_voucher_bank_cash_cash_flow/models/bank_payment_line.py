# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models


class BankPaymentLine(models.Model):
    _name = "account.bank_payment_line"
    _inherit = [
        "account.bank_payment_line",
        "account.voucher_line_common"
    ]
