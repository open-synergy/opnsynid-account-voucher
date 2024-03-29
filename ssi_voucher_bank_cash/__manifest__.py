# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Bank & Cash Accounting Voucher",
    "version": "14.0.2.2.1",
    "category": "Accounting",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_voucher_mixin",
        "account_payment",
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
        "data/sequence_template_bank_payment_data.xml",
        "data/sequence_template_bank_receipt_data.xml",
        "data/sequence_template_cash_payment_data.xml",
        "data/sequence_template_cash_receipt_data.xml",
        "data/approval_template_bank_payment_data.xml",
        "data/approval_template_bank_receipt_data.xml",
        "data/approval_template_cash_payment_data.xml",
        "data/approval_template_cash_receipt_data.xml",
        "data/policy_template_bank_payment_data.xml",
        "data/policy_template_bank_receipt_data.xml",
        "data/policy_template_cash_payment_data.xml",
        "data/policy_template_cash_receipt_data.xml",
        "views/account_voucher_common_views.xml",
        "views/account_bank_voucher_views.xml",
        "views/account_bank_receipt_views.xml",
        "views/account_bank_payment_views.xml",
        "views/account_cash_payment_views.xml",
        "views/account_cash_receipt_views.xml",
    ],
    "demo": [
        "demo/account_account_demo.xml",
        "demo/account_journal_demo.xml",
        "demo/account_voucher_type_allowed_journal_demo.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
}
