from odoo import models, fields, api

class Sale(models.Model):
    _inherit = 'sale.order'

    vat = fields.Char(related='partner_id.vat')
