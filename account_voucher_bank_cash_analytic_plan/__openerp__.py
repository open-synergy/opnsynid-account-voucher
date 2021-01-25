# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Bank & Cash Accounting Voucher Analytic Plan Feature",
    "version": "8.0.1.0.1",
    "category": "Accounting",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "auto_install": True,
    "depends": ["account_voucher_bank_cash", "account_voucher_common_analytic_plan"],
    "data": [
        "views/account_bank_payment_views.xml",
        "views/account_bank_receipt_views.xml",
        "views/account_cash_payment_views.xml",
        "views/account_cash_receipt_views.xml",
    ],
}
