# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class WizardPostVoucher(models.TransientModel):
    _name = "account.wizard_post_voucher"
    _description = "Wizard Post Voucher"

    date_post = fields.Date(
        string="Post Date",
        required=True,
    )

    @api.multi
    def action_post_voucher(self):
        self.ensure_one()
        active_model = self.env.context.get("active_model")
        active_id = self.env.context.get("active_id")
        vouchers = self.env[active_model].browse([active_id])
        vouchers.write(self._prepare_write_data())
        vouchers.workflow_action_post()

    @api.multi
    def _prepare_write_data(self):
        self.ensure_one()
        period = self.env["account.period"].find(self.date_post)
        result = {
            "date_voucher": self.date_post,
            "period_id": period.id,
        }
        return result
