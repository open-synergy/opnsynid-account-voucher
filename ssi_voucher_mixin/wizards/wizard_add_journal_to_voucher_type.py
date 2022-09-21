# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class WizardAddJurnalToVoucherType(models.TransientModel):
    _name = "account.wizard_add_journal_to_voucher_type"
    _description = "Add Journal To Voucher Type"

    type_id = fields.Many2one(
        string="Voucher Type",
        comodel_name="account.voucher_type",
        required=True,
    )

    def action_confirm(self):
        self.ensure_one()
        active_ids = self.env.context.get("active_ids", [])
        Journal = self.env["account.journal"]
        journals = Journal.browse(active_ids)
        journals.add_to_voucher_type(self.type_id)
