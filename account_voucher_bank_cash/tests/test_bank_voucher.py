# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date
from openerp.tests.common import TransactionCase


class TestBankVoucher(TransactionCase):

    def setUp(self, *args, **kwargs):
        result = super(TestBankVoucher, self).setUp(*args, **kwargs)

        self.bank_voucher_type = self.env.ref(
            "account_voucher_bank_cash.voucher_type_bank_receipt")

        self.bank_account = self.env["account.account"].create({
            "name": "X1",
            "code": "Test Bank Acc",
            "type": "liquidity",
            "user_type": self.env.ref("account.data_account_type_bank").id,
            "parent_id": self.env.ref("account.chart0").id,
        })

        self.income_account = self.env["account.account"].create({
            "name": "X2",
            "code": "Test Income Acc",
            "type": "other",
            "user_type": self.env.ref("account.data_account_type_income").id,
            "parent_id": self.env.ref("account.chart0").id,
        })

        self.receivable_account = self.env["account.account"].create({
            "name": "X3",
            "code": "Test Receivable Acc",
            "type": "receivable",
            "user_type": self.env.ref(
                "account.data_account_type_receivable").id,
            "parent_id": self.env.ref("account.chart0").id,
            "reconcile": True,
        })

        self.bank_journal = self.env["account.journal"].create({
            "code": "X1",
            "name": "Bank Journal",
            "type": "bank",
            "default_credit_account_id": self.bank_account.id,
            "default_debit_account_id": self.bank_account.id,
        })

        self.receivable_journal = self.env["account.journal"].create({
            "code": "X2",
            "name": "Sale Journal",
            "type": "sale",
        })

        self.partner = self.env["res.partner"].create({
            "name": "Test Partner",
        })

        self.bank_voucher_type.write({
            "allowed_journal_ids": [(0, 0, {
                "journal_id": self.bank_journal.id,
            })]
        })

        move_date = date.today().strftime("%Y-%m-%d")
        self.move = self.env["account.move"].create({
            "journal_id": self.receivable_journal.id,
            "date": move_date,
            "period_id": self.env["account.period"].find(move_date).id,
        })
        self.ml = self.env["account.move.line"].create({
            "move_id": self.move.id,
            "account_id": self.receivable_account.id,
            "partner_id": self.partner.id,
            "name": "test",
            "debit": 700.00,
            "credit": 0.0,
        })

        self.env["account.move.line"].create({
            "move_id": self.move.id,
            "account_id": self.income_account.id,
            "name": "test",
            "credit": 700.00,
            "debit": 0.0,
        })

        # Object
        self.obj_voucher = self.env["account.bank_voucher"]

        return result

    def _create_no_error(self):
        voucher_date = date.today().strftime("%Y-%m-%d")
        period = self.env["account.period"].find(voucher_date)
        voucher = self.env["account.bank_receipt"].create({
            "date_voucher": date.today().strftime("%Y-%m-%d"),
            "period_id": period.id,
            "journal_id": self.bank_journal.id,
            "account_id": self.bank_account.id,
            "amount": 700.00,
            "line_dr_ids": [(0, 0, {
                "type": "dr",
                "move_line_id": self.ml.id,
                "partner_id": self.partner.id,
                "account_id": self.receivable_account.id,
                "amount": 700.00,
                "name": "line",
            })]
        })
        self.assertEqual(voucher.state, "draft")
        return voucher

    def _confirm_no_error(self, voucher):
        voucher.workflow_action_confirm()
        self.assertEqual(voucher.state, "confirm")

    def _approve_no_error(self, voucher):
        voucher.workflow_action_approve()
        self.assertEqual(voucher.state, "approve")

    def _proforma_no_error(self, voucher):
        voucher.workflow_action_proforma()
        self.assertEqual(voucher.state, "proforma")

    def _cancel_no_error(self, voucher):
        voucher.workflow_action_cancel()
        self.assertEqual(voucher.state, "cancel")
        self.assertFalse(voucher.move_id)

    def _restart_no_error(self, voucher):
        voucher.workflow_action_restart()
        self.assertEqual(voucher.state, "draft")

    def _post_no_error(self, voucher):
        context = {
            "active_model": "account.bank_receipt",
            "active_id": voucher.id,
        }
        obj_wiz = self.env["account.wizard_post_voucher"]
        wiz = obj_wiz.with_context(context).create({
            "date_post": date.today().strftime("%Y-%m-%d"),
        })
        wiz.action_post_voucher()
        self.assertEqual(voucher.state, "post")
        self.assertNotEqual(voucher.move_id, False)

    def test_bank_voucher_flow_1(self):
        """
        test bank receipt workflow #1
        """
        bank_receipt = self._create_no_error()
        self._confirm_no_error(bank_receipt)
        self._approve_no_error(bank_receipt)
        self._post_no_error(bank_receipt)

    def test_bank_voucher_flow_2(self):
        """
        test bank receipt workflow #2
        """
        bank_receipt = self._create_no_error()
        self._confirm_no_error(bank_receipt)
        self._approve_no_error(bank_receipt)
        self._proforma_no_error(bank_receipt)
        self._post_no_error(bank_receipt)

    def test_bank_voucher_flow_3(self):
        """
        test bank receipt workflow #2
        """
        bank_receipt = self._create_no_error()
        self._confirm_no_error(bank_receipt)
        self._approve_no_error(bank_receipt)
        self._proforma_no_error(bank_receipt)
        self._post_no_error(bank_receipt)
        self._cancel_no_error(bank_receipt)
        self._restart_no_error(bank_receipt)
