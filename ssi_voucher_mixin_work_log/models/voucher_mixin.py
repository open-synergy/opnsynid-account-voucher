# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class MixinAccountVoucher(models.AbstractModel):
    _name = "mixin.account.voucher"
    _inherit = [
        "mixin.account.voucher",
        "mixin.work_object",
    ]

    _work_log_create_page = True
