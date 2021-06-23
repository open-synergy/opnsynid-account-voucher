# Copyright 2016-2019 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Common Accounting Voucher Feature",
    "version": "8.0.7.6.0",
    "category": "Accounting",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account",
        "base_sequence_configurator",
        "base_workflow_policy",
        "base_cancel_reason",
        "base_print_policy",
        "base_multiple_approval",
    ],
    "data": [
        "menu.xml",
        "security/ir.model.access.csv",
        "wizards/wizard_post_voucher.xml",
        "wizards/wizard_import_move_line.xml",
        "views/account_voucher_type_views.xml",
        "views/account_voucher_common_views.xml",
        "views/account_voucher_type_allowed_journal_views.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
}
