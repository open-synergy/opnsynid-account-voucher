# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class VoucherLineCommon(models.AbstractModel):
    _inherit = "account.voucher_line_common"

    @api.model
    def _default_analytic_account_id(self):
        partner_id = self.env.context.get("default_partner_id", False)
        analytic_default = self._get_analytic_default(
            partner_id=partner_id, user_id=self.env.user.id)
        return analytic_default and analytic_default.analytic_id

    analytic_account_id = fields.Many2one(
        default=lambda self: self._default_analytic_account_id(),
    )

    @api.model
    def _get_analytic_default(
            self, product_id=False, partner_id=False,
            user_id=False, date=False,
            company_id=False):
        obj_default = self.env["account.analytic.default"]
        analytic_default = obj_default.account_get(
            product_id=product_id, partner_id=partner_id,
            user_id=user_id, date=date, company_id=company_id)
        return analytic_default

    @api.onchange(
        "partner_id",
        "product_id",
    )
    def onchange_analytic_account_id(self):
        analytic_default = self._get_analytic_default(
            partner_id=self.partner_id and self.partner_id.id or False,
            product_id=self.product_id and self.product_id.id or False,
            user_id=self.env.user.id,
        )
        self.analytic_account_id = analytic_default and \
            analytic_default.analytic_id or False
