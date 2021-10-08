# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models


class CashReceiptLine(models.Model):
    _name = "account.cash_receipt_line"
    _inherit = ["account.cash_receipt_line", "account.voucher_line_common"]
