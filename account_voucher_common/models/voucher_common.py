# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError


class VoucherCommon(models.AbstractModel):
    _name = "account.voucher_common"
    _description = "Abstract Class for Accounting Voucher"
    _inherit = [
        "mail.thread",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
        "tier.validation",
    ]
    _state_from = ["draft", "confirm"]
    _state_to = ["approve"]

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.model
    def _default_date_voucher(self):
        return fields.Datetime.now()

    @api.multi
    def _compute_policy(self):
        _super = super(VoucherCommon, self)
        _super._compute_policy()

    @api.multi
    @api.depends(
        "type_id",
    )
    def _compute_allowed_journals(self):
        obj_allowed = self.env["account.voucher_type_allowed_journal"]
        for voucher in self:
            journal_ids = self.env["account.journal"].search([]).ids
            criteria = [
                ("voucher_type_id", "=", voucher.type_id.id),
                ("journal_id", "in", journal_ids),
            ]
            journal_ids = obj_allowed.search(criteria).mapped(
                lambda r: r.journal_id.id)
            voucher.allowed_journal_ids = journal_ids

    @api.multi
    @api.depends(
        "journal_id",
    )
    def _compute_currency_id(self):
        for voucher in self:
            currency_id = False
            if voucher.journal_id:
                journal = voucher.journal_id
                if journal.currency:
                    currency_id = journal.currency.id
                else:
                    currency_id = journal.company_id.currency_id.id
            voucher.currency_id = currency_id

    @api.multi
    @api.depends(
        "amount",
        "currency_id",
        "exchange_rate",
        "line_ids", "line_ids.amount",
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
            voucher.amount_diff_company_currency =\
                amount_diff_company_currency
            voucher.amount_diff = amount_diff
            voucher.amount_debit = debit
            voucher.amount_credit = credit

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
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        default=lambda self: self._default_company_id(),
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
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
    period_id = fields.Many2one(
        string="Period",
        comodel_name="account.period",
        required=True,
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
    amount = fields.Float(
        string="Total Voucher",
        readonly=True,
        default=1.0,
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
        comodel_name="account.voucher_line_common",
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
        comodel_name="account.voucher_line_common",
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
        comodel_name="account.voucher_line_common",
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
    note = fields.Text(
        strin="Notes",
    )
    move_id = fields.Many2one(
        string="Accounting Entry",
        comodel_name="account.move",
        readonly=True,
        copy=False,
    )
    move_line_ids = fields.One2many(
        string="Move Lines",
        comodel="account.move.line",
        related="move_id.line_id",
        readonly=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("approve", "Ready to Process"),
            ("proforma", "Proforma"),
            ("post", "Posted"),
            ("cancel", "Cancel"),
        ],
        required=True,
        readonly=True,
        default="draft",
        copy=False,
        track_visibility="onchange",
    )
    confirmed_date = fields.Datetime(
        string="Confirmation Date",
        readonly=True,
        copy=False,
    )
    confirmed_user_id = fields.Many2one(
        string="Confirmation By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    approved_date = fields.Datetime(
        string="Approval Date",
        readonly=True,
        copy=False,
    )
    approved_user_id = fields.Many2one(
        string="Approval By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    proforma_date = fields.Datetime(
        string="Proforma Date",
        readonly=True,
        copy=False,
    )
    proforma_user_id = fields.Many2one(
        string="Proforma By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    posted_date = fields.Datetime(
        string="Post Date",
        readonly=True,
        copy=False,
    )
    posted_user_id = fields.Many2one(
        string="Post By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    cancelled_date = fields.Datetime(
        string="Cancellation Date",
        readonly=True,
        copy=False,
    )
    cancelled_user_id = fields.Many2one(
        string="Cancellation By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
        store=False,
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
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
        store=False,
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
        store=False,
    )
    restart_validation_ok = fields.Boolean(
        string="Can Restart Validation",
        compute="_compute_policy",
    )

    @api.multi
    def workflow_action_confirm(self):
        for voucher in self:
            data = voucher._prepare_confirm_data()
            voucher.write(data)
            voucher.request_validation()

    @api.multi
    def workflow_action_approve(self):
        for voucher in self:
            data = voucher._prepare_approve_data()
            voucher.write(data)

    @api.multi
    def workflow_action_proforma(self):
        for voucher in self:
            data = voucher._prepare_proforma_data()
            voucher.write(data)

    @api.multi
    def workflow_action_post(self):
        for voucher in self:
            data = voucher._prepare_post_data()
            voucher.write(data)
            voucher._create_line_aml()

    @api.multi
    def workflow_action_cancel(self):
        for voucher in self:
            voucher._unreconcile_aml()
            if voucher._check_move():
                voucher.move_id.button_cancel()
            voucher.move_id.unlink()
            data = voucher._prepare_cancel_data()
            voucher.restart_validation()
            voucher.write(data)

    @api.multi
    def workflow_action_restart(self):
        for voucher in self:
            data = voucher._prepare_draft_data()
            voucher.write(data)

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        data = {
            "state": "confirm",
            "confirmed_date": fields.Datetime.now(),
            "confirmed_user_id": self.env.user.id,
        }
        return data

    @api.multi
    def _prepare_approve_data(self):
        self.ensure_one()
        data = {
            "state": "approve",
            "approved_date": fields.Datetime.now(),
            "approved_user_id": self.env.user.id,
        }
        return data

    @api.multi
    def _prepare_proforma_data(self):
        self.ensure_one()
        data = {
            "state": "proforma",
            "proforma_date": fields.Datetime.now(),
            "proforma_user_id": self.env.user.id,
        }
        return data

    @api.multi
    def _prepare_post_data(self):
        self.ensure_one()
        move = self.env["account.move"].create(
            self._prepare_account_move())
        data = {
            "state": "post",
            "move_id": move.id,
            "posted_date": fields.Datetime.now(),
            "posted_user_id": self.env.user.id,
        }
        return data

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        data = {
            "state": "cancel",
            "cancelled_date": fields.Datetime.now(),
            "cancelled_user_id": self.env.user.id,
        }
        return data

    @api.multi
    def _prepare_draft_data(self):
        self.ensure_one()
        data = {
            "state": "draft",
            "confirmed_date": False,
            "confirmed_user_id": False,
            "approved_date": False,
            "approved_user_id": False,
            "proforma_date": False,
            "proforma_user_id": False,
            "posted_date": False,
            "posted_user_id": False,
            "cancelled_date": False,
            "cancelled_user_id": False,
        }
        return data

    @api.constrains(
        "type_id",
        "amount_diff",
        "state",
    )
    def _check_total(self):
        if self.state == "confirm" and self.type_id.check_total and \
                not self.currency_id.is_zero(self.amount_diff) and \
                not self.writeoff_account_id:
            raise UserError(_("There are still amount difference"))

    @api.model
    def create(self, values):
        _super = super(VoucherCommon, self)
        result = _super.create(values)
        sequence = result._create_sequence()
        result.write({
            "name": sequence,
        })
        return result

    @api.constrains("partner_id", "line_ids")
    def _check_partner(self):
        str_error = _("Line partner is different from header partner")
        if self.partner_id:
            partner = self.partner_id
            for line in self.line_ids:
                if line.partner_id != partner:
                    raise UserError(str_error)

    @api.constrains("amount", "type_id")
    def _check_negative_value(self):
        str_error = _("Header value has to be greater than 0")
        if not self.type_id.header_allow_negative and \
                self.amount < 0:
            raise UserError(str_error)

    @api.multi
    def _check_header_negative_value(self):
        self.ensure_one()

    @api.onchange("date_voucher")
    def onchange_date(self):
        self.period_id = self.env[
            "account.period"].find(self.date_voucher).id

    @api.multi
    def _check_move(self):
        self.ensure_one()
        result = False
        if self.move_id.state == "posted":
            result = True
        return result

    @api.multi
    def _unreconcile_aml(self):
        self.ensure_one()
        for aml in self.move_line_ids:
            aml.refresh()
            reconcile = aml.reconcile_id or aml.reconcile_partial_id or \
                False
            if reconcile:
                move_lines = reconcile.line_id
                move_lines -= aml
                reconcile.unlink()

                if len(move_lines) >= 2:
                    move_lines.reconcile_partial()

    @api.onchange(
        "journal_id")
    def onchange_journal(self):
        self.account_id = False
        vtype = self.type_id
        if self.journal_id:
            journal = self.journal_id
            if vtype.header_type:
                if vtype.header_type == "dr":
                    self.account_id = journal.default_debit_account_id and \
                        journal.default_debit_account_id.id or False
                elif vtype.header_type == "cr":
                    self.account_id = journal.default_credit_account_id and \
                        journal.default_credit_account_id.id or False

    @api.multi
    def _check_total_voucher(self):
        self.ensure_one()
        result = True
        vtype = self.type_id
        obj_currency = self.env["res.currency"]

        if vtype.check_total and obj_currency.is_zero(
                self.company_id.currency_id,
                self.diff_amount_in_company_currency):
            result = False
        return result

    @api.constrains(
        "amount_debit", "amount_credit",
        "type_id", "state")
    def _check_debit_credit(self):
        str_error = _("Unequal debit credit")
        if self.type_id.check_debit_credit and \
                (self.amount_debit != self.amount_credit) and \
                self.state == "confirm":
            raise UserError(str_error)

    @api.multi
    def _prepare_account_move(self):
        self.ensure_one()
        data = {
            "name": self.name,
            "ref": self.name,
            "date": self.date_voucher,
            "period_id": self.period_id.id,
            "journal_id": self.journal_id.id,
            "line_id": self._prepare_move_line(),
        }
        return data

    @api.multi
    def _prepare_move_line(self):
        self.ensure_one()
        data = []
        vtype = self.type_id
        writeoff_account =\
            self.writeoff_account_id

        if vtype.create_header_item:
            data.append((0, 0, self._prepare_move_header()))
        if writeoff_account and \
                not self.currency_id.is_zero(self.amount_diff):
            data.append((0, 0, self._prepare_writeoff_header()))
        return data

    @api.multi
    def _create_line_aml(self):
        self.ensure_one()
        pairs = []
        for line in self.line_ids:
            result = line._create_aml()
            if result:
                pairs.append(result)
        for pair in pairs:
            pair.reconcile_partial()

    @api.multi
    def _prepare_move_header(self):
        self.ensure_one()
        debit, credit = self._get_header_debit_credit()
        partner_id = self.partner_id and \
            self.partner_id.commercial_partner_id.id or \
            False
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

    @api.multi
    def _prepare_writeoff_header(self):
        self.ensure_one()
        debit, credit = self._get_writeoff_debit_credit()
        partner_id = self.partner_id and \
            self.partner_id.commercial_partner_id.id or \
            False
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

    @api.multi
    def _get_move_currency(self):
        self.ensure_one()
        result = False
        if self.currency_id != self.company_currency_id:
            result = self.currency_id.id
        return result

    @api.multi
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

    @api.multi
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

    @api.multi
    def _get_header_debit_credit(self):
        self.ensure_one()
        debit = credit = 0.0
        vtype = self.type_id
        if vtype.header_type == "dr":
            debit = self.amount_in_company_currency
        elif vtype.header_type == "cr":
            credit = self.amount_in_company_currency
        return (debit, credit)

    @api.multi
    def _get_writeoff_debit_credit(self):
        self.ensure_one()
        debit = credit = 0.0
        vtype = self.type_id
        amount_diff_company_currency =\
            self.amount_diff_company_currency

        if amount_diff_company_currency < 0:
            if vtype.header_type == "dr":
                debit = abs(
                    amount_diff_company_currency)
            elif vtype.header_type == "cr":
                credit = abs(
                    amount_diff_company_currency)
        else:
            if vtype.header_type == "dr":
                credit = abs(
                    amount_diff_company_currency)
            elif vtype.header_type == "cr":
                debit = abs(
                    amount_diff_company_currency)
        return (debit, credit)

    @api.multi
    def unlink(self):
        strWarning = _("You can only delete data on draft state")
        for voucher in self:
            if voucher.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning)
        _super = super(VoucherCommon, self)
        _super.unlink()

    @api.multi
    def validate_tier(self):
        _super = super(VoucherCommon, self)
        _super.validate_tier()
        for document in self:
            if document.validated:
                document.workflow_action_approve()

    @api.multi
    def restart_validation(self):
        _super = super(VoucherCommon, self)
        _super.restart_validation()
        for document in self:
            document.request_validation()
