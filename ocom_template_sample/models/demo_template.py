# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class TestModel(models.Model):
    _name = 'test.model1'
    _description = 'Test model'
    name = fields.Char()
    name_test = fields.Char()
    tl_id = fields.Many2one('test.line1')
    tl_ids = fields.Many2many('test.line1')
    tlo_ids = fields.One2many('test.line1','tm_id')

    def button_1(self):
        pass
    
class TestLine(models.Model):
    _name = 'test.line1'
    _description = 'Test Line'
    name = fields.Char()
    tm_id = fields.Many2one('test.model1')
    
    