# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.tools.safe_eval import safe_eval

from collections import defaultdict, OrderedDict
from odoo.exceptions import AccessError, MissingError, ValidationError, UserError
from odoo.tools import frozendict, lazy_classproperty, ormcache, \
                   Collector, LastOrderedSet, OrderedSet, IterableGenerator, \
                   groupby

class TestModel(models.Model):
    _name = 'test.model'
    _description = 'test model'

    domain = fields.Char(default=[])
    name = fields.Char(ndtsize=1, size=90, required=1)
    name_test = fields.Char(translate=1)
    name_test2 = fields.Char(compute='_compute_name_test2', store=1)
    # name_test3 = fields.Char(compute='_compute_name_test2', store=1)

    simple_compute_test = fields.Char(compute='_simple_compute_test', store=1)
    tl_ids = fields.Many2many('test.line','testline_test_model_rel','test_model_id','test_line_id',string='tlm ids')
    tl2_ids = fields.Many2many('test.line','testline_test_model_rel2',
        'test_model_id', 'test_line_id', compute='_compute_tl2_ids', store=True)
    tlo_ids = fields.One2many('test.line','tm_id')
    depend_field = fields.Char(compute='_compute_depend_field')
    tl_id = fields.Many2one('test.line', auto_join=True)
    oc = fields.Char()
    oc_result = fields.Char()
    no_store_compute_field = fields.Char(compute='_compute_no_store_compute_field')
    number = fields.Float(digits=(6,0))
    
    # @api.model
    # def flush(self, fnames=None, records=None):
    #     print ('***self._name', self._name, 'fnames', fnames,'records', records )
    #     return super().flush(fnames, records)

    @api.model
    def flush(self, fnames=None, records=None):
        """ Process all the pending computations (on all models), and flush all
        the pending updates to the database.

        :param fnames (list<str>): list of field names to flush.  If given,
            limit the processing to the given fields of the current model.
        :param records (Model): if given (together with ``fnames``), limit the
            processing to the given records.
        """
        def process(model, id_vals):
            print ('***id_vals***', id_vals)
            # group record ids by vals, to update in batch when possible
            updates = defaultdict(list)
            for rid, vals in id_vals.items():
                updates[frozendict(vals)].append(rid)

            for vals, ids in updates.items():
                recs = model.browse(ids)
                try:
                    recs._write(vals)
                except MissingError:
                    recs.exists()._write(vals)

        if fnames is None:
            # flush everything
            self.recompute()
            while self.env.all.towrite:
                model_name, id_vals = self.env.all.towrite.popitem()
                process(self.env[model_name], id_vals)
        else:
            # flush self's model if any of the fields must be flushed
            self.recompute(fnames, records=records)

            # check whether any of 'records' must be flushed
            if records is not None:
                fnames = set(fnames)
                towrite = self.env.all.towrite.get(self._name)
                if not towrite or all(
                    fnames.isdisjoint(towrite.get(record.id, ()))
                    for record in records
                ):
                    return

            # DLE P76: test_onchange_one2many_with_domain_on_related_field
            # ```
            # email.important = True
            # self.assertIn(email, discussion.important_emails)
            # ```
            # When a search on a field coming from a related occurs (the domain
            # on discussion.important_emails field), make sure the related field
            # is flushed
            model_fields = {}
            for fname in fnames:
                field = self._fields[fname]
                model_fields.setdefault(field.model_name, []).append(field)
                if field.related_field:
                    model_fields.setdefault(field.related_field.model_name, []).append(field.related_field)
            for model_name, fields in model_fields.items():
                if any(
                    field.name in vals
                    for vals in self.env.all.towrite.get(model_name, {}).values()
                    for field in fields
                ):
                    id_vals = self.env.all.towrite.pop(model_name)
                    process(self.env[model_name], id_vals)

            # missing for one2many fields, flush their inverse
            for fname in fnames:
                field = self._fields[fname]
                if field.type == 'one2many' and field.inverse_name:
                    self.env[field.comodel_name].flush([field.inverse_name])



    def write(self, *args,**kwargs):
        print ('write.........', 'args',args,'***kwargs***', kwargs)
        return super(TestModel,self).write(*args,**kwargs)


    def _write(self, *args,**kwargs):
        print ('args',args,'***kwargs***', kwargs)
        return super(TestModel,self)._write(*args,**kwargs)

    def _simple_compute_test(self):
        # r = self
        # r.simple_compute_test = 'ahahaha'
        for r in self:
            if r.name:
                r.simple_compute_test = '%s prefix'%r.name 

    #test.model.name: {None: {test.model.no_store_compute_field, test.model.tl2_ids

    def test(self):
        raise UserError('adkfdfjlkdfjkld')
        o = self.search([], limit=1)
        o.name = 1
        o.name_test = 2
        # domain = safe_eval(self.domain)
        # print ('***domain***', domain)
        # # rs = self.env['test.model'].search([('name','=','a'),('number','=',1)])
        # rs = self.env['test.model'].search(domain)
        # print ('rs',rs)
        # self.write({'number': 1.21})
        # for i in range(4):
        #     print (self.tl2_ids)

    def test2(self):
        self.write({'name':3, 'name_test':4})

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
            # r.name_test = 'dau xanh'# cái này sao ăn luôn ta?
            # r.write({'name_test': 'dieu gi do'})

    @api.depends('tl_ids.name', 'tlo_ids.employee_id.name')#,'tlo_ids', 'tlo_ids.employee_id.name'; test.line.name: {test.model.tl_ids: {None: {test.model.name_test2}}
    #(test.model.tl_ids,), (test.model.tl_ids, test.line.name), (test.model.tlo_ids,), (test.model.tlo_ids, test.line.tm_id), (test.model.tlo_ids, test.line.employee_id), (test.model.tlo_ids, test.line.employee_id, res.partner.name)
    def _compute_name_test2(self):
        for r in self:
            if r.tl_ids:
                r.name_test2 = r.tl_ids.mapped('name')
            elif r.tlo_ids:
                r.name_test2 = r.tlo_ids.mapped('name')

class TestLine(models.Model):
    _name = 'test.line'
    # _description = 'test line'

    name = fields.Char()
    tm_id = fields.Many2one('test.model')
    employee_id = fields.Many2one('res.partner')

    # @api.onchange('employee_id')
    # def _onchange_employee_id(self):
    #     for r in self:
    #         r.name = r.employee_id.name
    #         r.tm_id.name_test = r.employee_id.name


