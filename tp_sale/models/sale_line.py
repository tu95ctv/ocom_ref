from odoo import models, fields, api

class SaleLine(models.Model):
    _name = 'tp.sale.line'
    _description = 'TP sale'

    product_id = fields.Many2one('product.product')
    qty = fields.Integer()
    price_unit = fields.Float(digits=(6,2))
    price = fields.Float(compute='_compute_price', store=True)
    sale_id = fields.Many2one('tp.sale')

    @api.depends('qty', 'price_unit')
    def _compute_price(self):
        for record in self:
            record.price = record.qty * record.price_unit
 