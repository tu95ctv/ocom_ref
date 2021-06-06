# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class Trade(models.Model):
    _name = 'ck.trade'
    _description = 'User Trade'

    partner_id = fields.Many2one()
    type = fields.Selection([('buy','Buy'),('sale','Sale')])
    trade_line_ids = fields.One2many('ck.trade','trade_id')
    

class TradeLine(models.Model):
    _name = 'ck.trade.line'
    





    
    
    