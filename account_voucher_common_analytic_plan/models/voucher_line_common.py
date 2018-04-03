# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class VoucherLineCommon(models.AbstractModel):
    _inherit = "account.voucher_line_common"

    @api.model
    def _default_analytic_plan_account_id(self):
        partner_id = self.env.context.get("default_partner_id", False)
        analytic_default = self._get_analytic_default(
            partner_id=partner_id, user_id=self.env.user.id)
        return analytic_default and analytic_default.analytics_id

    analytic_plan_account_id = fields.Many2one(
        string="Analytic Plan",
        comodel_name="account.analytic.plan.instance"
    )

    @api.onchange(
        "partner_id",
        "product_id",
    )
    def onchange_plan_account_id(self):
        analytic_default = self._get_analytic_default(
            partner_id=self.partner_id and self.partner_id.id or False,
            product_id=self.product_id and self.product_id.id or False,
            user_id=self.env.user.id,
        )
        self.analytic_plan_account_id = analytic_default and \
            analytic_default.analytics_id or False

    @api.onchange(
        "partner_id",
        "product_id",
    )
    def onchange_analytic_account_id(self):
        self.analytic_account_id = False

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
