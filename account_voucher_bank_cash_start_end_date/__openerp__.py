# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Bank & Cash Accounting Voucher Start & End Date Feature",
    "version": "8.0.1.0.0",
    "category": "Accounting",
    "website": "https://opensynergy-indonesia.com/",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "auto_install": True,
    "depends": [
        "account_voucher_bank_cash",
        "account_voucher_common_start_end_date"
    ],
    "data": [
        "views/account_bank_payment_views.xml",
        "views/account_bank_receipt_views.xml",
        "views/account_cash_payment_views.xml",
        "views/account_cash_receipt_views.xml",
    ],
}
