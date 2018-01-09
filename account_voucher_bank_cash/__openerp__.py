# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Bank & Cash Accounting Voucher",
    "version": "8.0.1.4.0",
    "category": "Accounting",
    "website": "https://opensynergy-indonesia.com/",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account_voucher_common",
        "account_payment",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/account_voucher_type_data.xml",
        "views/account_voucher_common_views.xml",
        "views/account_bank_voucher_views.xml",
        "views/account_bank_receipt_views.xml",
        "views/account_bank_payment_views.xml",
        "views/account_cash_payment_views.xml",
        "views/account_cash_receipt_views.xml",
    ],
}
