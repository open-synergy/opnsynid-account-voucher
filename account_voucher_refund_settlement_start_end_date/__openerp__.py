# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Refund Settlement Accounting Voucher Start & End Date Feature",
    "version": "8.0.1.0.0",
    "category": "Accounting",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "auto_install": True,
    "depends": [
        "account_voucher_refund_settlement",
        "account_voucher_common_start_end_date",
    ],
    "data": [
        "views/account_sale_refund_settlement_views.xml",
        "views/account_purchase_refund_settlement_views.xml",
    ],
}
