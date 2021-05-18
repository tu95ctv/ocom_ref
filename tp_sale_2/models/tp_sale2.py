# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class TPSale2(models.Model):
    _inherit = 'tp.sale'

    tpsale2 = fields.Char()


    
    