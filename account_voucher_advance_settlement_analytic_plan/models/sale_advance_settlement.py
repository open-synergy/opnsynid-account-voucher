# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models


class SaleAdvanceSettlementLine(models.Model):
    _name = "account.sale_advance_settlement_line"
    _inherit = [
        "account.voucher_line_common",
        "account.sale_advance_settlement_line"
    ]


class SaleAdvanceSettlementLineTax(models.Model):
    _name = "account.sale_advance_settlement_line_tax"
    _inherit = [
        "account.sale_advance_settlement_line_tax",
        "account.voucher_line_tax_common"
    ]
