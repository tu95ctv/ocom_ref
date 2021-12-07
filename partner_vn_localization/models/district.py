# -*- coding: utf-8 -*-

from odoo import api, fields, models
import re


class State(models.Model):
    _inherit = 'res.country.state'
    # _order = 'code'

    name_without_prefix = fields.Char(compute='_name_without_prefix', store=True)

    # @api.one
    @api.depends('name')
    def _name_without_prefix(self):
        for r in self:
            r.name_without_prefix = re.sub('(^Tỉnh |^Thủ đô |^Thành phố |^tp )', '', r.name, flags=re.I)



class District(models.Model):
    _description = 'District'
    _name = 'res.country.district'
    # _order = 'id desc'

    state_id = fields.Many2one('res.country.state', string='Province', required=True)
    active = fields.Boolean(default=True)
    name = fields.Char(string='District Name', required=True)
    code = fields.Char(string='District Code', required=True)
    name_without_prefix = fields.Char(compute='_name_without_prefix', store=True)

    # @api.one
    @api.depends('name')
    def _name_without_prefix(self):
        for r in self:
            r.name_without_prefix = re.sub('(^Quận |^Huyện |^Thành phố |^tp )', '', r.name, flags=re.I)
            

    