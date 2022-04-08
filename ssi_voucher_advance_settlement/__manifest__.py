# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Advance Settlement Voucher",
    "version": "14.0.1.2.0",
    "category": "Accounting",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "ssi_voucher_settlement_common",
    ],
    "data": [
        "security/ir.model.access.csv",
        "menu.xml",
        "data/account_voucher_type_data.xml",
        "data/ir_windows_action_data.xml",
        "data/ir_sequence_data.xml",
        "data/sequence_template_purchase_settlement_data.xml",
        "data/sequence_template_sale_settlement_data.xml",
        "data/approval_template_purchase_settlement_data.xml",
        "data/approval_template_sale_settlement_data.xml",
        "data/policy_template_purchase_settlement_data.xml",
        "data/policy_template_sale_settlement_data.xml",
        "views/account_sale_advance_settlement_views.xml",
        "views/account_purchase_advance_settlement_views.xml",
    ],
    "demo": [
        "demo/account_journal_demo.xml",
        "demo/account_voucher_type_allowed_journal_demo.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
}
