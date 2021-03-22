# -*- coding: utf-8 -*-
from operator import attrgetter
from odoo import fields

class CounterChar(fields.Char):
    _slots = {
        'counter_size':None
    }
    _related_counter_size = property(attrgetter('counter_size'))
    _description_counter_size = property(attrgetter('counter_size'))