# -*- coding: utf-8 -*-
from odoo import models, fields, api

class EM(models.Model):
    _inherit = 'hr.employee'

    test_number = fields.Integer()
    test_number2 = fields.Integer()


