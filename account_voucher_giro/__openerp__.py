# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Giro Accounting Voucher",
    "version": "8.0.1.1.0",
    "category": "Accounting",
    "website": "https://opensynergy-indonesia.com/",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account_voucher_bank_cash",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/account_voucher_type_data.xml",
        "views/account_giro_voucher_views.xml",
        "views/account_giro_receipt_views.xml",
        "views/account_giro_payment_views.xml",
    ],
}
