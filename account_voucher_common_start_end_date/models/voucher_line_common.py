# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class VoucherLineCommon(models.AbstractModel):
    _inherit = "account.voucher_line_common"

    date_start = fields.Date(string="Start Date")
    date_end = fields.Date(string="End Date")

    @api.multi
    def _prepare_move_line(self):
        res = super(VoucherLineCommon, self)._prepare_move_line()
        res["start_date"] = self.date_start or False
        res["end_date"] = self.date_end or False
        return res

    @api.multi
    def _prepare_exchange_move_line(self):
        res = super(VoucherLineCommon, self)._prepare_exchange_move_line()
        res["start_date"] = self.date_start or False
        res["end_date"] = self.date_end or False
        return res
