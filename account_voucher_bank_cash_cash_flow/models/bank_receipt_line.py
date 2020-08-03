# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class BankReceiptLine(models.Model):
    _inherit = "account.bank_receipt_line"

    direct_cash_flow_id = fields.Many2one(
        string="Direct Cash Flow",
        comodel_name="account.cash_flow_code",
        domain=[
            ("type", "=", "direct"),
        ],
    )
    indirect_cash_flow_id = fields.Many2one(
        string="Indirect Cash Flow",
        comodel_name="account.cash_flow_code",
        domain=[
            ("type", "=", "indirect"),
        ],
    )

    @api.multi
    def _prepare_move_line(self):
        _super = super(BankReceiptLine, self)
        res = _super._prepare_move_line()
        res["direct_cash_flow_id"] = self.direct_cash_flow_id.id
        res["indirect_cash_flow_id"] = self.indirect_cash_flow_id.id
        return res

    @api.multi
    def _prepare_exchange_move_line(self):
        _super = super(BankReceiptLine, self)
        res = _super._prepare_exchange_move_line()
        res["direct_cash_flow_id"] = self.direct_cash_flow_id.id
        res["indirect_cash_flow_id"] = self.indirect_cash_flow_id.id
        return res
