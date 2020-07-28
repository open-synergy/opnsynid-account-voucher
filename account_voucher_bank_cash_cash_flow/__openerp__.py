# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Bank & Cash Accounting Voucher - Cash Flow",
    "version": "8.0.1.0.0",
    "category": "Accounting",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "account_voucher_bank_cash",
        "account_cash_flow_code",
    ],
    "data": [
        "views/account_cash_receipt_views.xml",
        "views/account_bank_receipt_views.xml",
        "views/account_cash_payment_views.xml",
        "views/account_bank_payment_views.xml",
    ],
}
