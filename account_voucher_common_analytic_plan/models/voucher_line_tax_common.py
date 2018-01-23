# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api


class VoucherLineTaxCommon(models.AbstractModel):
    _inherit = "account.voucher_line_tax_common"

    @api.multi
    def _prepare_move_line(self):
        res = super(VoucherLineTaxCommon, self)._prepare_move_line()
        vline = self.voucher_line_id
        res["analytics_id"] = \
            vline.analytic_plan_account_id and \
            vline.analytic_plan_account_id.id or \
            False
        return res
