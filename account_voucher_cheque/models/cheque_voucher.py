# -*- coding: utf-8 -*-
# Copyright 2017-2019 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class ChequeVoucher(models.AbstractModel):
    _name = "account.cheque_voucher"
    _inherit = "account.voucher_common"
    _description = "Cheque Voucher"

    name = fields.Char(
        string="# Cheque",
    )
    date_issue = fields.Date(
        string="Date Issued",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    source_bank_id = fields.Many2one(
        string="Source Bank Account",
        comodel_name="res.partner.bank",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    payee_partner_id = fields.Many2one(
        string="Payee",
        comodel_name="res.partner",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    partner_id = fields.Many2one(
        required=True,
    )

    @api.onchange(
        "company_id", "type_id", "partner_id",
    )
    def onchange_source_bank_id(self):
        obj_partner = self.env["res.partner"]
        domain = {
            "source_bank_id": [
                ("id", "=", 0),
            ]
        }
        self.source_bank_id = False
        if self.company_id and self.type_id and self.partner_id:
            if self.type_id.header_type == "dr":
                commercial_partner = self.partner_id.commercial_partner_id
                criteria = [
                    ("commercial_partner_id", "=", commercial_partner.id),
                ]
            elif self.type_id.header_type == "cr":
                commercial_partner = self.company_id.partner_id.\
                    commercial_partner_id
                criteria = [
                    ("commercial_partner_id", "=", commercial_partner.id),
                ]
            partner_ids = obj_partner.search(criteria).ids
            domain["source_bank_id"] = [
                ("partner_id", "in", partner_ids),
            ]

        return {"domain": domain}
