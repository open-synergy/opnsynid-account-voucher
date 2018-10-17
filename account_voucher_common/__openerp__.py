# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Common Accounting Voucher Feature",
    "version": "8.0.5.3.1",
    "category": "Accounting",
    "website": "https://opensynergy-indonesia.com/",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizards/wizard_post_voucher.xml",
        "wizards/wizard_import_move_line.xml",
        "views/account_voucher_type_views.xml",
        "views/account_voucher_common_views.xml",
    ],
}
