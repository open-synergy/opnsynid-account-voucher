# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class VoucherLineTaxCommon(models.AbstractModel):
    _inherit = "account.voucher_line_tax_common"

    @api.multi
    def _prepare_move_line(self):
        res = super(VoucherLineTaxCommon, self)._prepare_move_line()
        vline = self.voucher_line_id
        res["start_date"] = vline.date_start or False
        res["end_date"] = vline.date_end or False
        return res
