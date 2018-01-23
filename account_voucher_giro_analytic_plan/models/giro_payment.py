# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models


class GiroPaymentLine(models.Model):
    _name = "account.giro_payment_line"
    _inherit = "account.voucher_line_common"

class GiroPaymentLineTax(models.Model):
    _name = "account.giro_payment_line_tax"
    _inherit = "account.voucher_line_tax_common"
