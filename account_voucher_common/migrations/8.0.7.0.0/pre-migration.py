# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


def migrate(cr, version):
    if not version:
        return
    if openupgrade.table_exists(cr, "rel_vtype_journal_approve_group"):
        openupgrade.logged_query(
            cr,
            """
            DROP TABLE rel_vtype_journal_approve_group CASCADE
            """,
        )
