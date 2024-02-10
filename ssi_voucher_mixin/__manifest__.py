# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Account Voucher Mixin",
    "version": "14.0.1.7.0",
    "category": "Accounting",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account",
        "mail",
        "ssi_master_data_mixin",
        "ssi_transaction_confirm_mixin",
        "ssi_transaction_done_mixin",
        "ssi_transaction_cancel_mixin",
        "ssi_transaction_open_mixin",
    ],
    "data": [
        "menu.xml",
        "security/ir.model.access.csv",
        "wizards/wizard_post_voucher.xml",
        "wizards/wizard_import_move_line.xml",
        "wizards/wizard_add_journal_to_voucher_type.xml",
        "views/account_voucher_type_views.xml",
        "views/mixin_account_voucher_views.xml",
        "views/account_voucher_type_allowed_journal_views.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
}
