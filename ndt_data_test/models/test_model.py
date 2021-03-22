# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class TestModel(models.Model):
    _name = 'test.model'
    _description = 'test model'

    name = fields.Char(ndtsize=1, size=90, required=1)
    name_test = fields.Char(translate=1)
    name_test2 = fields.Char(compute='_compute_name_test2', store=1)
    simple_compute_test = fields.Char(compute='_simple_compute_test', store=1)
    tl_ids = fields.Many2many('test.line','testline_test_model_rel','test_model_id','test_line_id',string='tlm ids')
    tl2_ids = fields.Many2many('test.line','testline_test_model_rel2',
        'test_model_id', 'test_line_id', compute='_compute_tl2_ids', store=True)
    tlo_ids = fields.One2many('test.line','tm_id')
    depend_field = fields.Char(compute='_compute_depend_field')
    tl_id = fields.Many2one('test.line')
    oc = fields.Char()
    oc_result = fields.Char()
    no_store_compute_field = fields.Char(compute='_compute_no_store_compute_field')

    def _simple_compute_test(self):
        # r = self
        # r.simple_compute_test = 'ahahaha'
        for r in self:
            if r.name:
                r.simple_compute_test = '%s prefix'%r.name 

    #test.model.name: {None: {test.model.no_store_compute_field, test.model.tl2_ids
    def test(self):
        for i in range(4):
            print (self.tl2_ids)

    @api.depends('name')
    def _compute_no_store_compute_field(self):
        for r in self:
            print ('<<_compute_no_store_compute_field')
            r.no_store_compute_field = 2

    @api.depends('name')
    def _compute_tl2_ids(self):
        for r in self:
            l1 = self.env['test.line'].search([])
            # r.write({'tl2_ids' :[(6,0,l1.ids)]})
            r.tl2_ids = [(6,0,l1.ids)]

    @api.onchange('oc')
    def _onchange_oc(self):
        if self.oc:
            self.oc_result = 2*self.oc

    @api.depends('name','tl_id')
    def _compute_depend_field(self):
        for r in self:
            r.depend_field = self.name + ' ahaha' if self.name else 'khong co gi'
            r.name_test = 'dau xanh'
            # r.write({'name_test': 'dieu gi do'})

    @api.depends('tl_ids.name')#,'tlo_ids', 'tlo_ids.employee_id.name'; test.line.name: {test.model.tl_ids: {None: {test.model.name_test2}}
    def _compute_name_test2(self):
        for r in self:
            if r.tl_ids:
                r.name_test2 = r.tl_ids.mapped('name')
            elif r.tlo_ids:
                r.name_test2 = r.tlo_ids.mapped('name')
    
class TestLine(models.Model):
    _name = 'test.line'
    name = fields.Char()
    tm_id = fields.Many2one('test.model')
    employee_id = fields.Many2one('res.partner')

    # @api.onchange('employee_id')
    # def _onchange_employee_id(self):
    #     for r in self:
    #         r.name = r.employee_id.name
    #         r.tm_id.name_test = r.employee_id.name


