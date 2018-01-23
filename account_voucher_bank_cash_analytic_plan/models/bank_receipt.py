# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models


class BankReceiptLine(models.Model):
    _name = "account.bank_receipt_line"
    _inherit = "account.voucher_line_common"

class BankReceiptLineTax(models.Model):
    _name = "account.bank_receipt_line_tax"
    _inherit = "account.voucher_line_tax_common"
