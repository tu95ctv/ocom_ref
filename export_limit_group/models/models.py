# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class export_limit_group(models.Model):
#     _name = 'export_limit_group.export_limit_group'
#     _description = 'export_limit_group.export_limit_group'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
