# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class WizardPostVoucher(models.TransientModel):
    _name = "account.wizard_post_voucher"
    _description = "Wizard Post Voucher"

    date_post = fields.Date(
        string="Post Date",
        required=True,
    )

    def action_post_voucher(self):
        self.ensure_one()
        active_model = self.env.context.get("active_model")
        active_id = self.env.context.get("active_id")
        vouchers = self.env[active_model].browse([active_id])
        vouchers.write(self._prepare_write_data())
        vouchers.action_done()

    def _prepare_write_data(self):
        self.ensure_one()
        result = {
            "date_voucher": self.date_post,
        }
        return result
