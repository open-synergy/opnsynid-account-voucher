# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class AccountJournal(models.Model):
    _name = "account.journal"
    _inherit = "account.journal"

    def add_to_voucher_type(self, voucher_type):
        for record in self:
            record._add_to_voucher_type(voucher_type)

    def _add_to_voucher_type(self, voucher_type):
        self.ensure_one()
        AllowedJournal = self.env["account.voucher_type_allowed_journal"]
        AllowedJournal.create(
            {
                "voucher_type_id": voucher_type.id,
                "journal_id": self.id,
            }
        )
