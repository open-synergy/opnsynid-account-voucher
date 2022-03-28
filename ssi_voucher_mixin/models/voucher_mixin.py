# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MixinAccountVoucher(models.AbstractModel):
    _name = "mixin.account.voucher"
    _description = "Abstract Class for Accounting Voucher"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_cancel",
        "mixin.transaction_open",
    ]
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"
    _create_sequence_state = "open"

    @api.model
    def _get_policy_field(self):
        res = super(MixinAccountVoucher, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "open_ok",
            "proforma_ok",
            "approve_ok",
            "post_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
        ]
        res += policy_field
        return res

    @api.depends("policy_template_id")
    def _compute_policy(self):
        _super = super(MixinAccountVoucher, self)
        _super._compute_policy()

    name = fields.Char(
        string="# Voucher",
        default="/",
        copy=False,
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    description = fields.Char(
        string="Description",
        required=True,
        default="/",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.model
    def _default_date_voucher(self):
        return fields.Datetime.now()

    date_voucher = fields.Date(
        string="Date",
        required=True,
        default=lambda self: self._default_date_voucher(),
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    writeoff_account_id = fields.Many2one(
        string="Write-Off Account",
        comodel_name="account.account",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        domain=[
            ("type", "not in", ["view", "consolidation", "closed"]),
        ],
    )
    type_id = fields.Many2one(
        string="Voucher Type",
        comodel_name="account.voucher_type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.depends(
        "type_id",
    )
    def _compute_allowed_journals(self):
        obj_allowed_journal = self.env["account.voucher_type_allowed_journal"]
        obj_account_journal = self.env["account.journal"]
        for voucher in self:
            journal_ids = obj_account_journal.search([]).ids
            criteria = [
                ("voucher_type_id", "=", voucher.type_id.id),
                ("journal_id", "in", journal_ids),
            ]
            journal_ids = obj_allowed_journal.search(criteria).mapped(
                lambda r: r.journal_id.id
            )
            voucher.allowed_journal_ids = journal_ids

    allowed_journal_ids = fields.Many2many(
        string="Allowed Journals",
        comodel_name="account.journal",
        compute="_compute_allowed_journals",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.depends(
        "journal_id",
    )
    def _compute_currency_id(self):
        for voucher in self:
            currency_id = False
            if voucher.journal_id:
                journal = voucher.journal_id
                if journal.currency_id:
                    currency_id = journal.currency_id.id
                else:
                    currency_id = journal.company_id.currency_id.id
            voucher.currency_id = currency_id

    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        compute="_compute_currency_id",
        store=True,
    )
    company_currency_id = fields.Many2one(
        string="Company Currency",
        comodel_name="res.currency",
        readonly=True,
    )

    @api.depends(
        "amount",
        "currency_id",
        "exchange_rate",
        "line_ids",
        "line_ids.amount",
        "line_ids.move_line_id",
        "line_ids.amount_before_tax",
        "line_ids.amount_tax",
        "line_ids.amount_after_tax",
    )
    def _compute_amount(self):
        for voucher in self:
            amount_company_currency = 0.0
            line_total = 0.0
            debit = credit = 0.0
            amount_company_currency = voucher.amount * voucher.exchange_rate
            voucher.amount_in_company_currency = amount_company_currency

            for line in voucher.line_ids:
                line_total += line.amount_after_tax
                if line.type == "dr":
                    debit += line.amount_after_tax
                else:
                    credit += line.amount_after_tax

            amount_diff = voucher.amount - line_total
            amount_diff_company_currency = amount_diff * voucher.exchange_rate
            voucher.amount_diff_company_currency = amount_diff_company_currency
            voucher.amount_diff = amount_diff
            voucher.amount_debit = debit
            voucher.amount_credit = credit

    amount = fields.Float(
        string="Total Voucher",
        readonly=True,
        default=0.0,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    exchange_rate = fields.Float(
        string="Exchange Rate",
        default=1.0,
        readonly=True,
        digits=(12, 6),
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    amount_in_company_currency = fields.Float(
        string="Total Voucher in Company Currency",
        compute="_compute_amount",
        store=True,
    )
    amount_diff = fields.Float(
        string="Amount Diff.",
        compute="_compute_amount",
        store=True,
    )
    amount_diff_company_currency = fields.Float(
        string="Amount Diff. in Company Currency",
        compute="_compute_amount",
        store=True,
    )
    amount_debit = fields.Float(
        string="Debit",
        compute="_compute_amount",
        store=True,
    )
    amount_credit = fields.Float(
        string="Credit",
        compute="_compute_amount",
        store=True,
    )
    line_ids = fields.One2many(
        string="Voucher Line",
        comodel_name="mixin.account.voucher.line",
        inverse_name="voucher_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    line_dr_ids = fields.One2many(
        string="Debit",
        comodel_name="mixin.account.voucher.line",
        inverse_name="voucher_id",
        domain=[
            ("type", "=", "dr"),
        ],
        context={
            "default_type": "dr",
        },
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    line_cr_ids = fields.One2many(
        string="Credit",
        comodel_name="mixin.account.voucher.line",
        inverse_name="voucher_id",
        domain=[
            ("type", "=", "cr"),
        ],
        context={
            "default_type": "cr",
        },
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    move_id = fields.Many2one(
        string="Accounting Entry",
        comodel_name="account.move",
        readonly=True,
        copy=False,
    )
    move_line_ids = fields.One2many(
        string="Move Lines",
        related="move_id.line_ids",
        readonly=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "On Progress"),
            ("proforma", "Proforma"),
            ("post", "Posted"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
        ],
        required=True,
        readonly=True,
        default="draft",
        copy=False,
        track_visibility="onchange",
    )
    proforma_ok = fields.Boolean(
        string="Can Proforma",
        compute="_compute_policy",
        store=False,
    )
    post_ok = fields.Boolean(
        string="Can Post",
        compute="_compute_policy",
        store=False,
    )

    def action_cancel(self, cancel_reason=False):
        _super = super(MixinAccountVoucher, self)
        res = _super.action_cancel(cancel_reason)
        for voucher in self:
            voucher._unreconcile_aml()
            if voucher._check_move():
                voucher.move_id.button_cancel()
            voucher.move_id.with_context(force_delete=True).unlink()
        return res

    def action_proforma(self):
        for voucher in self:
            data = voucher._prepare_proforma_data()
            voucher.write(data)

    def action_post(self):
        for voucher in self:
            data = voucher._prepare_post_data()
            voucher.write(data)
            voucher._create_line_aml()

    def _prepare_proforma_data(self):
        self.ensure_one()
        data = {
            "state": "proforma",
        }
        return data

    def _prepare_post_data(self):
        self.ensure_one()
        obj_account_move = self.env["account.move"]
        move = obj_account_move.create(self._prepare_account_move())
        data = {
            "state": "post",
            "move_id": move.id,
        }
        return data

    @api.constrains(
        "type_id",
        "amount_diff",
        "state",
    )
    def _check_total(self):
        str_error = _("There are still amount difference")
        for document in self:
            if (
                document.state == "confirm"
                and document.type_id.check_total
                and not document.currency_id.is_zero(document.amount_diff)
                and not document.writeoff_account_id
            ):
                raise UserError(str_error)

    @api.constrains("partner_id", "line_ids")
    def _check_partner(self):
        str_error = _("Line partner is different from header partner")
        for document in self:
            if document.partner_id:
                partner = document.partner_id
                for line in document.line_ids:
                    if line.partner_id != partner:
                        raise UserError(str_error)

    @api.constrains("amount", "type_id")
    def _check_negative_value(self):
        str_error = _("Header value has to be greater than 0")
        for document in self:
            header_allow_negative = document.type_id.header_allow_negative
            if not header_allow_negative and self.amount < 0:
                raise UserError(str_error)

    @api.constrains(
        "exchange_rate",
    )
    def _check_exchange_rate(self):
        str_error = _("Exchange rate value has to be greater than 0")
        for document in self:
            if document.exchange_rate <= 0:
                raise UserError(str_error)

    def _check_header_negative_value(self):
        self.ensure_one()

    def _check_move(self):
        self.ensure_one()
        result = False
        if self.move_id.state == "posted":
            result = True
        return result

    def _unreconcile_aml(self):
        self.ensure_one()
        for aml in self.move_line_ids:
            aml.remove_move_reconcile()

    @api.onchange(
        "type_id",
    )
    def onchange_policy_template_id(self):
        template_id = self._get_template_policy()
        self.policy_template_id = template_id

    @api.onchange("journal_id")
    def onchange_account_id(self):
        self.account_id = False
        vtype = self.type_id
        if self.journal_id:
            journal = self.journal_id
            if vtype.header_type:
                if vtype.header_type == "dr":
                    self.account_id = (
                        journal.payment_debit_account_id
                        and journal.payment_debit_account_id.id
                        or False
                    )
                elif vtype.header_type == "cr":
                    self.account_id = (
                        journal.payment_credit_account_id
                        and journal.payment_credit_account_id.id
                        or False
                    )

    def _check_total_voucher(self):
        self.ensure_one()
        result = True
        vtype = self.type_id
        obj_currency = self.env["res.currency"]

        if vtype.check_total and obj_currency.is_zero(
            self.company_id.currency_id, self.diff_amount_in_company_currency
        ):
            result = False
        return result

    @api.constrains("name")
    def _check_name(self):
        obj_voucher = self.env[self._name]
        for record in self:
            str_error = _("Document " + record.name + " has been used")
            if record.name != "/":
                criteria = [("name", "=", record.name), ("id", "!=", record.id)]
                data = obj_voucher.search(criteria)
                if data:
                    raise UserError(str_error)

    @api.constrains("amount_debit", "amount_credit", "type_id", "state")
    def _check_debit_credit(self):
        for document in self:
            str_error = _("Unequal debit credit")
            if (
                document.type_id.check_debit_credit
                and (document.amount_debit != document.amount_credit)
                and document.state == "confirm"
            ):
                raise UserError(str_error)

    def _prepare_account_move(self):
        self.ensure_one()
        data = {
            "name": self.name,
            "ref": self.name,
            "date": self.date_voucher,
            "journal_id": self.journal_id.id,
            "line_ids": self._prepare_move_line(),
        }
        return data

    def _prepare_move_line(self):
        self.ensure_one()
        data = []
        vtype = self.type_id
        writeoff_account = self.writeoff_account_id

        if vtype.create_header_item:
            data.append((0, 0, self._prepare_move_header()))
        if writeoff_account and not self.currency_id.is_zero(self.amount_diff):
            data.append((0, 0, self._prepare_writeoff_header()))
        return data

    def _create_line_aml(self):
        self.ensure_one()
        pairs = []
        for line in self.line_ids:
            result = line._create_aml()
            if result:
                pairs.append(result)
        self.move_id.post()
        for pair in pairs:
            pair.reconcile()

    def _prepare_move_header(self):
        self.ensure_one()
        debit, credit = self._get_header_debit_credit()
        partner_id = (
            self.partner_id and self.partner_id.commercial_partner_id.id or False
        )
        data = {
            "name": self.description,
            "debit": debit,
            "credit": credit,
            "account_id": self.account_id.id,
            "amount_currency": self._get_header_amount_currency(),
            "currency_id": self._get_move_currency(),
            "partner_id": partner_id,
        }
        return data

    def _prepare_writeoff_header(self):
        self.ensure_one()
        debit, credit = self._get_writeoff_debit_credit()
        partner_id = (
            self.partner_id and self.partner_id.commercial_partner_id.id or False
        )
        data = {
            "name": "Write-Off " + self.description,
            "debit": debit,
            "credit": credit,
            "account_id": self.writeoff_account_id.id,
            "amount_currency": self._get_writeoff_amount_currency(),
            "currency_id": self._get_move_currency(),
            "partner_id": partner_id,
        }
        return data

    def _get_move_currency(self):
        self.ensure_one()
        result = False
        if self.currency_id != self.company_currency_id:
            result = self.currency_id.id
        return result

    def _get_header_amount_currency(self):
        self.ensure_one()
        result = 0.0
        vtype = self.type_id
        if self.currency_id != self.company_currency_id:
            if vtype.header_type == "dr":
                result = self.amount
            else:
                result = -1.0 * self.amount
        return result

    def _get_writeoff_amount_currency(self):
        self.ensure_one()
        result = 0.0
        vtype = self.type_id
        if self.currency_id != self.company_currency_id:
            if vtype.header_type == "dr":
                result = self.amount_diff
            else:
                result = -1.0 * self.amount_diff
        return result

    def _get_header_debit_credit(self):
        self.ensure_one()
        debit = credit = 0.0
        vtype = self.type_id
        if vtype.header_type == "dr":
            debit = self.amount_in_company_currency
        elif vtype.header_type == "cr":
            credit = self.amount_in_company_currency
        return (debit, credit)

    def _get_writeoff_debit_credit(self):
        self.ensure_one()
        debit = credit = 0.0
        vtype = self.type_id
        amount_diff_company_currency = self.amount_diff_company_currency

        if amount_diff_company_currency < 0:
            if vtype.header_type == "dr":
                debit = abs(amount_diff_company_currency)
            elif vtype.header_type == "cr":
                credit = abs(amount_diff_company_currency)
        else:
            if vtype.header_type == "dr":
                credit = abs(amount_diff_company_currency)
            elif vtype.header_type == "cr":
                debit = abs(amount_diff_company_currency)
        return (debit, credit)

    def action_approve_approval(self):
        _super = super(MixinAccountVoucher, self)
        _super.action_approve_approval()
        for document in self:
            if document.approved:
                document.action_open()
