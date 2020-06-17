# -*- coding: utf-8 -*-
# Copyright 2017-2019 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError


class GiroVoucher(models.AbstractModel):
    _name = "account.giro_voucher"
    _inherit = "account.voucher_common"
    _description = "Giro Voucher"

    name = fields.Char(
        string="# Giro",
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
    date_due = fields.Date(
        string="Date Due",
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
    destination_bank_id = fields.Many2one(
        string="Destination Bank Account",
        comodel_name="res.partner.bank",
        required=False,
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

    @api.constrains(
        "state", "date_due", "date_voucher",
    )
    def _check_no_post_before_due(self):
        if self.state == "post" and \
                (self.date_voucher < self.date_due):
            raise UserError(_("You cannot post giro before due date"))

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

    @api.onchange(
        "company_id", "type_id", "partner_id",
    )
    def onchange_destination_bank_id(self):
        obj_partner = self.env["res.partner"]
        domain = {
            "destination_bank_id": [
                ("id", "=", 0),
            ]
        }
        self.source_bank_id = False
        if self.company_id and self.type_id and self.partner_id:
            if self.type_id.header_type == "cr":
                commercial_partner = self.partner_id.commercial_partner_id
                criteria = [
                    ("commercial_partner_id", "=", commercial_partner.id),
                ]
            elif self.type_id.header_type == "dr":
                commercial_partner = self.company_id.partner_id.\
                    commercial_partner_id
                criteria = [
                    ("commercial_partner_id", "=", commercial_partner.id),
                ]
            partner_ids = obj_partner.search(criteria).ids
            domain["destination_bank_id"] = [
                ("partner_id", "in", partner_ids),
            ]

        return {"domain": domain}
