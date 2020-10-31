# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api

class TileTile(models.Model):
    _name = 'tile.tile'
    _description = 'Dashboard Tile'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=0, required=True)
#    user_id = fields.Many2one('res.users', 'User')
    background_color = fields.Char(default='#0E6C7E', oldname='color')
    font_color = fields.Char(default='#FFFFFF')

    model_id = fields.Many2one('ir.model', 'Model', required=True)
    domain = fields.Text(default='[]')
    action_id = fields.Many2one('ir.actions.act_window', 'Action')

    active = fields.Boolean(
#        compute='_compute_active',
#        search='_search_active',
        readonly=True)

    # Primary Value
    primary_function = fields.Selection(
        FIELD_FUNCTION_SELECTION,
        string='Function',
        default='count')
    primary_field_id = fields.Many2one(
        'ir.model.fields',
        string='Field',
        domain="[('model_id', '=', model_id),"
               " ('ttype', 'in', ['float', 'integer'])]")
    primary_format = fields.Char(
        string='Format',
        help='Python Format String valid with str.format()\n'
             'ie: \'{:,} Kgs\' will output \'1,000 Kgs\' if value is 1000.')
    primary_value = fields.Char(
        string='Value',
        compute='_compute_data')
    primary_helper = fields.Char(
        string='Helper',
        compute='_compute_helper')

    # Secondary Value
    secondary_function = fields.Selection(
        FIELD_FUNCTION_SELECTION,
        string='Secondary Function')
    secondary_field_id = fields.Many2one(
        'ir.model.fields',
        string='Secondary Field',
        domain="[('model_id', '=', model_id),"
               " ('ttype', 'in', ['float', 'integer'])]")
    secondary_format = fields.Char(
        string='Secondary Format',
        help='Python Format String valid with str.format()\n'
             'ie: \'{:,} Kgs\' will output \'1,000 Kgs\' if value is 1000.')
    secondary_value = fields.Char(
        string='Secondary Value',
        compute='_compute_data')
    secondary_helper = fields.Char(
        string='Secondary Helper',
        compute='_compute_helper')
