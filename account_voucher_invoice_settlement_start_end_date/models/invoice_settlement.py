# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models


class InvoiceSettlementLine(models.Model):
    _name = "account.invoice_settlement_line"
    _inherit = ["account.invoice_settlement_line", "account.voucher_line_common"]


class InvoiceSettlementLineTax(models.Model):
    _name = "account.invoice_settlement_line_tax"
    _inherit = [
        "account.invoice_settlement_line_tax",
        "account.voucher_line_tax_common",
    ]
