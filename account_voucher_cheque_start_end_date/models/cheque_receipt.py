# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models


class ChequeReceiptLine(models.Model):
    _name = "account.cheque_receipt_line"
    _inherit = [
        "account.cheque_receipt_line",
        "account.voucher_line_common"
    ]


class ChequeReceiptLineTax(models.Model):
    _name = "account.cheque_receipt_line_tax"
    _inherit = [
        "account.cheque_receipt_line_tax",
        "account.voucher_line_tax_common"
    ]
