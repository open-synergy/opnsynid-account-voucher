# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class VoucherLineCommon(models.AbstractModel):
    _inherit = "account.voucher_line_common"

    analytic_plan_account_id = fields.Many2one(
        string="Analytic Plan",
        comodel_name="account.analytic.plan.instance"
    )

    @api.multi
    def _prepare_move_line(self):
        res = super(VoucherLineCommon, self)._prepare_move_line()
        res["analytics_id"] = \
            self.analytic_plan_account_id and \
            self.analytic_plan_account_id.id or \
            False
        return res

    @api.multi
    def _prepare_exchange_move_line(self):
        res = super(VoucherLineCommon, self)._prepare_exchange_move_line()
        res["analytics_id"] = \
            self.analytic_plan_account_id and \
            self.analytic_plan_account_id.id or \
            False
        return res
