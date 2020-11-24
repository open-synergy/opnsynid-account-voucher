# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Refund Settlement Accounting Voucher - Dashboard and Tile",
    "version": "8.0.1.0.0",
    "category": "Accounting",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "web_dashboard_tile",
        "account_voucher_refund_settlement",
    ],
    "data": [
        "data/dashboard_tile_account_voucher_refund_settlement_data.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
}
