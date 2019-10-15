# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Advance Settlement Voucher",
    "version": "8.0.1.2.0",
    "category": "Accounting",
    "website": "https://opensynergy-indonesia.com/",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account_voucher_settlement_common",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/account_voucher_type_data.xml",
        "data/ir_sequence_data.xml",
        "data/base_sequence_configurator_data.xml",
        "data/base_workflow_policy_sale_advance_data.xml",
        "data/base_workflow_policy_purchase_advance_data.xml",
        "data/base_cancel_reason_configurator_data.xml",
        "views/account_sale_advance_settlement_views.xml",
        "views/account_purchase_advance_settlement_views.xml",
    ],
}
