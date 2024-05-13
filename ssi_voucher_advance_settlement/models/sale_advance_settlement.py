# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class SaleAdvanceSettlement(models.Model):
    _name = "account.sale_advance_settlement"
    _inherit = "mixin.account.voucher"
    _description = "Sale Advance Settlement"

    @api.model
    def _default_type_id(self):
        return self.env.ref(
            "ssi_voucher_advance_settlement." "voucher_type_sale_advance_settlement"
        ).id

    type_id = fields.Many2one(
        default=lambda self: self._default_type_id(),
    )
    company_currency_id = fields.Many2one(
        string="Company Currency",
        comodel_name="res.currency",
        related="company_id.currency_id",
        store=True,
    )
    line_ids = fields.One2many(
        comodel_name="account.sale_advance_settlement_line",
    )
    line_summary_ids = fields.One2many(
        comodel_name="account.sale_advance_settlement_line_summary",
    )
    line_dr_ids = fields.One2many(
        comodel_name="account.sale_advance_settlement_line",
    )
    line_cr_ids = fields.One2many(
        comodel_name="account.sale_advance_settlement_line",
    )


class SaleAdvanceSettlementLine(models.Model):
    _name = "account.sale_advance_settlement_line"
    _inherit = "mixin.account.voucher.line"
    _description = "Sale Advance Settlement Line"

    voucher_id = fields.Many2one(
        comodel_name="account.sale_advance_settlement",
    )
    tax_ids = fields.One2many(
        comodel_name="account.sale_advance_settlement_line_tax",
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        related="voucher_id.currency_id",
        store=True,
    )
    company_currency_id = fields.Many2one(
        comodel_name="res.currency",
        related="voucher_id.company_currency_id",
        store=True,
    )


class SaleAdvanceSettlementLineTax(models.Model):
    _name = "account.sale_advance_settlement_line_tax"
    _inherit = "mixin.account.voucher.line.tax"
    _description = "Sale Advance Settlement Line Tax"

    voucher_line_id = fields.Many2one(
        comodel_name="account.sale_advance_settlement_line",
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        related="voucher_line_id.currency_id",
        store=True,
    )
    company_currency_id = fields.Many2one(
        comodel_name="res.currency",
        related="voucher_line_id.company_currency_id",
        store=True,
    )


class SaleAdvanceSettlementLineSummary(models.Model):
    _name = "account.sale_advance_settlement_line_summary"
    _inherit = "mixin.account.voucher.line.summary"
    _description = "Sale Advance Settlement Line Summary"
    _auto = False

    voucher_id = fields.Many2one(
        comodel_name="account.sale_advance_settlement",
    )

    def _select(self):
        select_str = """
        SELECT
            row_number() OVER() as id,
            a.voucher_id AS voucher_id,
            a.account_id AS account_id,
            a.partner_id AS partner_id,
            a.currency_id AS currency_id,
            SUM(a.amount_before_tax) AS amount_before_tax,
            SUM(a.amount_tax) AS amount_tax,
            SUM(a.amount_after_tax) AS amount_after_tax
        """
        return select_str

    def _get_from_table(self):
        return "account_sale_advance_settlement_line"

    def _from(self):
        from_str = """
        %s AS a
        """ % (
            self._get_from_table()
        )
        return from_str

    def _where(self):
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join(self):
        join_str = """
        """
        return join_str

    def _group_by(self):
        group_str = """
        GROUP BY a.voucher_id,a.account_id,a.partner_id,a.currency_id
        """
        return group_str

    def init(self):
        # tools.drop_view_if_exists(self._cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        self._cr.execute(
            """CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            %s
            %s
        )"""
            % (
                self._table,
                self._select(),
                self._from(),
                self._join(),
                self._where(),
                self._group_by(),
            )
        )
