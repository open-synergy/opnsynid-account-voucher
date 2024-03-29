# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Invoice Settlement Voucher",
    "version": "14.0.2.3.0",
    "category": "Accounting",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_voucher_settlement_common",
        "ssi_financial_accounting",
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
        "data/sequence_template_data.xml",
        "data/approval_template_data.xml",
        "data/policy_template_data.xml",
        "data/account_journal_data.xml",
        "data/account_voucher_type_allowed_journal_data.xml",
        "views/account_invoice_settlement_views.xml",
    ],
    "demo": [
        "demo/account_journal_demo.xml",
        "demo/account_voucher_type_allowed_journal_demo.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
}
