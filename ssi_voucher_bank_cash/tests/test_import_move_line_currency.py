# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestImportMoveLineCurrency(YamlTransactionCase):
    """Test currency conversion on the Import Move Lines wizard.

    Covers ``account.wizard_import_move_line.action_import_move_line()``
    and ``mixin.account.voucher.line._compute_amount()`` for the case
    where the imported ``account.move.line`` is denominated in a
    currency different from the destination voucher's currency
    (cross-currency bridging), and confirms same-currency
    reconciliation stays unaffected.
    """

    def test_import_move_line_currency(self):
        """Run the cross-currency Import Move Lines scenario."""
        self.run_yaml_scenario("test_data_import_move_line_currency.yaml")
