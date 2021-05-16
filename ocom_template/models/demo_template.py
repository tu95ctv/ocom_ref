# -*- coding: utf-8 -*-
from odoo import models, fields, api
import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round
from time import sleep
import threading
from operator import attrgetter

import logging
_logger = logging.getLogger(__name__)

from odoo.addons.counter_widget.models.fields import CounterChar

def get_report_card_limit_remark(env):
    return env['ir.config_parameter'].sudo().get_param('report_card_limit_remark')

class TestModel1(models.Model):
    _name = 'test.model1'
    name = CounterChar(counter_size=get_report_card_limit_remark, size=50)
    name_test = fields.Char()
    tl_ids = fields.Many2many('test.line1','testline_test_model1_rel','test_line1_id','test_model1_id')
    tlo_ids = fields.One2many('test.line1','tm_id')
    tl_id = fields.Many2one('test.line1', domain=[('name','ilike','a')])
    def button_1(self):
        pass
    
class TestLine(models.Model):
    _name = 'test.line1'
    name = fields.Char()
    tm_id = fields.Many2one('test.model1')
    
    