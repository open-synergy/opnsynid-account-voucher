# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Giro Accounting Voucher",
    "version": "14.0.2.1.0",
    "category": "Accounting",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "ssi_voucher_bank_cash",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "security/ir_rule_data.xml",
        "security/ir.model.access.csv",
        "menu.xml",
        "data/account_voucher_type_data.xml",
        "data/ir_windows_action_data.xml",
        "data/ir_sequence_data.xml",
        "data/sequence_template_giro_payment_data.xml",
        "data/sequence_template_giro_receipt_data.xml",
        "data/approval_template_giro_payment_data.xml",
        "data/approval_template_giro_receipt_data.xml",
        "data/policy_template_giro_payment_data.xml",
        "data/policy_template_giro_receipt_data.xml",
        "views/account_giro_voucher_views.xml",
        "views/account_giro_receipt_views.xml",
        "views/account_giro_payment_views.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
}
