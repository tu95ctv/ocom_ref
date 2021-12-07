# -*- coding: utf-8 -*-

from odoo import api, fields, models
import re

class Ward(models.Model):
    _description = 'Ward'
    _name = 'res.country.ward'
    _order = 'code'

    district_id = fields.Many2one('res.country.district', string='District', required=True)
    active = fields.Boolean(default=True)
    name = fields.Char(string='Ward Name', required=True)
    code = fields.Char(string='Ward Code', required=True)
    name_without_prefix = fields.Char(compute='_name_without_prefix', store=True)

    # @api.one
    @api.depends('name')
    def _name_without_prefix(self):
        for r in self:
            r.name_without_prefix = re.sub('(^Phường |^Xã |^Thành phố |^Thị trấn )', '', r.name, flags=re.I)

