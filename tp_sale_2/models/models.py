# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools
import logging
_logger = logging.getLogger(__name__)

class TPSale2(models.Model):
    _inherit = 'tp.sale.order'

    a1 = fields.Integer()
    a2 = fields.Char(string="abc")
    # b1 = fields.Char(string='by')
    x1 = fields.Char()
    # @tools.ormcache('self.env.uid', 'self.env.su')
    def test_cache(self):
        res = super().test_cache()
        print ('res của test cache trước super ', res)
        print ('test_cache 3')
        return 3

    # @api.depends('number')
    # def _compute_b1(self):
    #     for r in self:
    #         r.b1 = 3*r.a
    #         r.c = r.a

    @api.onchange('customer_id','number')
    def _oc_customer_id(self):
        print (2222222222)
        super()._oc_customer_id()



    # @api.depends('line_ids')
    # def _compute_amount(self):
    #     for rec in self:
    #         rec.amount = sum(rec.line_ids.mapped('price'))

    
    # @api.depends('a')
    # def _b(self):
    #     for r in self:
    #         r.b = 20*r.a + 2
    #         # r.c = r.a
    #         r.line_ids.qty = r.a

    
    