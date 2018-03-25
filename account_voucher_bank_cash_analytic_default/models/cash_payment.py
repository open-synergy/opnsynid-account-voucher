# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models


class CashPaymentLine(models.Model):
    _name = "account.cash_payment_line"
    _inherit = [
        "account.cash_payment_line",
        "account.voucher_line_common"
    ]
