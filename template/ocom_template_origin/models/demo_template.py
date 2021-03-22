# -*- coding: utf-8 -*-
from odoo import models, fields, api
import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round
from time import sleep
import threading

import logging
_logger = logging.getLogger(__name__)

def return_this_view_wrap(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        func(*args, **kwargs)
        return self.return_this_view()
    return wrapper



class CreatDataTest(models.TransientModel):
    _name = 'ndt.data.test'
    _description = 'Create data test'

    
    test_env = {}
    rs = fields.Text()

class TestModel1(models.Model):
    _name = 'test.model'
    name = fields.Char()
    name_test = fields.Char()
    tl_ids = fields.Many2many('test.line','testline_test_model_rel','test_line_id','test_model_id')
    tlo_ids = fields.One2many('test.line','tm_id')
    
class TestLine(models.Model):
    _name = 'test.line'
    name = fields.Char()
    tm_id = fields.Many2one('test.model')
    
    