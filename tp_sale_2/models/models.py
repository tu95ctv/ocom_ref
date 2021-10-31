# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class TPSale2(models.Model):
    _inherit = 'tp.sale.order'


    @api.depends('line_ids')
    def _compute_amount(self):
        for rec in self:
            rec.amount = sum(rec.line_ids.mapped('price'))

    
    