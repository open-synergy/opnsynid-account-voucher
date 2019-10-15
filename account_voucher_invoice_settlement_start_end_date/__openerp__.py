# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Invoice Settlement Voucher Integration With "
            "Start & End Date Feature",
    "version": "8.0.1.0.0",
    "category": "Accounting",
    "website": "https://opensynergy-indonesia.com/",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "auto_install": True,
    "depends": [
        "account_voucher_invoice_settlement",
        "account_voucher_common_start_end_date"
    ],
    "data": [
        "views/account_invoice_settlement_views.xml",
    ],
}