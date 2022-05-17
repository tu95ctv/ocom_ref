
from odoo import fields,models,api

class Cron(models.Model):
    _inherit = 'ir.cron'

    def reset_stock_quant(self):
        qs = self.env['stock.quant'].search([('location_id.name','in',('Work Center Openning','Work Center Closing'))])
        print (qs,'qs')
        qs.with_context(inventory_mode=True).inventory_quantity = 0 
        qs.with_context(inventory_mode=True).reserved_quantity = 0 

    def reset_stock_quant_all(self):
        qs = self.env['stock.quant'].search([('location_id.name','in',('Work Center Openning','Work Center Closing','Work Center Material'))])
        print (qs,'qs')
        qs.with_context(inventory_mode=True).inventory_quantity = 0 
        qs.with_context(inventory_mode=True).reserved_quantity = 0 
