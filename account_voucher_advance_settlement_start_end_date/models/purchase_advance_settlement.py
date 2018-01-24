# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models


class PurchaseAdvanceSettlementLine(models.Model):
    _name = "account.purchase_advance_settlement_line"
    _inherit = [
        "account.purchase_advance_settlement_line",
        "account.voucher_line_common"
    ]

class PurchaseAdvanceSettlementLineTax(models.Model):
    _name = "account.purchase_advance_settlement_line_tax"
    _inherit = [
        "account.purchase_advance_settlement_line_tax",
        "account.voucher_line_tax_common"
    ]
