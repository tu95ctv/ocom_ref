# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from time import sleep
from odoo.tools import config
from datetime import date
import logging
_logger = logging.getLogger(__name__)
import threading
import inspect
from odoo.addons.restful.common import RevenueRecognizeLog
from odoo.tools import ormcache, ormcache_context
# class User(models.Model):
#     _inherit = 'res.users' #tên bàng tp_sale

#     new_field = fields.Char()

class Contact(models.Model):
    _inherit = 'res.partner' #tên bàng tp_sale
    
    def print_abc(self):
        print ('abc', config['data_dir'],'haha',config.filestore('o141'))

    # @api.model
    # @ormcache_context('str(views)','str(options)', keys=('lang',))
    # def load_views(self, views, options=None):
    #     print ('*load_views*'*100)
    #     rs = super(Contact, self).load_views(views,options)
    #     return rs

class SaleParent(models.Model):
    _name = 'tp.sale.order.parent' #tên bàng tp_sale

    xyz = fields.Char()


class Sale(models.Model):
    _name = 'tp.sale.order' #tên bàng tp_sale
    _description = 'TP sale'
    # _inherit=['xmlidab.xmlidab']
    # _inherit = ['mail.thread.cc']


    # _inherits = {'tp.sale.order.parent': 'tp_sale_parent_id'}
    # amount = fields.Float(compute='_compute_amount', store=True)
    amount = fields.Float(compute='_compute_amount', store=True)
    @api.depends('line_ids.price','m2m_a_line_ids')
    def _compute_amount(self):
        for rec in self:
            rec.amount = sum(rec.line_ids.mapped('price'))
    line_ids = fields.One2many('tp.sale.order.line', 'order_id')
    ref_line_ids = fields.One2many('tp.sale.order.line', 'res_id')
    image_test = fields.Binary(attachment=False)
    name = fields.Char(default='anh nhơ me')
    customer_id = fields.Many2one('res.partner', domain=[('id','in',(3,4))], auto_join=True)
    order_date = fields.Date()  
    number = fields.Float(digits=(6,2))
    a = fields.Integer()
    b = fields.Integer(compute='_b', store=1, groups='hr.group_hr_manager')
    c = fields.Integer(compute='_c', store=1)
    d = fields.Integer()
    attachment_ids = fields.One2many('ir.attachment','res_id')
    line_id = fields.Many2one('tp.sale.order.line')
    name_line = fields.Char(related='line_id.name', store=True)
    m2m_line_ids = fields.Many2many('tp.sale.order.line','so_sol_rel','so_id','sol_id')
    m2m_a_line_ids = fields.Many2many('tp.sale.order.line',compute='_compute_m2m_a_line_ids',
        store=True)
    number2 = fields.Integer()
    # dt = fields.Datetime(default=fields.Datetime.now, string="Ngày giờ")
    dt = fields.Date()
    nr = fields.Integer('Number required', required=True, default=1)
    cr = fields.Char('Char required', required=True,default=1)

    @api.depends('number2')
    def _compute_m2m_a_line_ids(self):
        self.m2m_a_line_ids = False


    # @api.model
    # def load_views(self, views, options=None):
    #     """ Returns the fields_views of given views, along with the fields of
    #         the current model, and optionally its filters for the given action.

    #     :param views: list of [view_id, view_type]
    #     :param options['toolbar']: True to include contextual actions when loading fields_views
    #     :param options['load_filters']: True to return the model's filters
    #     :param options['action_id']: id of the action to get the filters
    #     :return: dictionary with fields_views, fields and optionally filters
    #     """
    #     options = options or {}
    #     result = {}

    #     toolbar = options.get('toolbar')
    #     result['fields_views'] = {
    #         v_type: self.fields_view_get(v_id, v_type if v_type != 'list' else 'tree',
    #                                      toolbar=toolbar if v_type != 'search' else False)
    #         for [v_id, v_type] in views
    #     }
    #     result['fields'] = self.fields_get()

    #     if options.get('load_filters'):
    #         result['filters'] = self.env['ir.filters'].get_filters(self._name, options.get('action_id'))


    #     return result

    

    @api.model
    @ormcache('str(views)','str(options)')
    def load_views(self, views, options=None):
        print ('*load_views*'*100)
        rs = super(Sale, self).load_views(views,options)
        return rs
        # options = options or {}
        # result = {}

        # toolbar = options.get('toolbar')
        # result['fields_views'] = {
        #     v_type: self.fields_view_get(v_id, v_type if v_type != 'list' else 'tree',
        #                                  toolbar=toolbar if v_type != 'search' else False)
        #     for [v_id, v_type] in views
        # }
        # result['fields'] = self.fields_get()

        # if options.get('load_filters'):
        #     result['filters'] = self.env['ir.filters'].get_filters(self._name, options.get('action_id'))


        # return result

    
    @api.onchange('number')
    def _onchange_number(self):
        print ('self.id', self.id, bool(self.id),'self.ids',self.ids, 'self.m2m_line_ids',self.m2m_line_ids,self.m2m_line_ids.ids)
        print ('self.b', self.b)
        if self.number:
            rs = self.env['tp.sale.order.line'].search([], limit=self.number, order='id desc')
            self.line_ids = rs
            self.line_ids = [(0,0,{'product_id':1, 'qty':100})]
            self.line_ids = [(1,1,{'product_id':1, 'qty':1000})]

    # b = fields.Integer(store=True)
    # c = fields.Integer(store=False)
    # d = fields.Integer(store=False)
    e = fields.Integer()
    
    @api.depends('a', 'c', 'm2m_line_ids','line_ids')
    def _b(self):
        print ("inspect.stack()[1][3]", inspect.stack()[1][3])
        print ('_b')
        for r in self:
            r.b = r.a
            r.a = 2*r.b

    @api.depends('b')
    def _c(self):
        print ('_c')
        for r in self:
            r.c = r.b
            r.a = 2*r.c 
           
          


    # @api.depends('e')
    # def _d(self):
    #     print ('self',self)
    #     for r in self:
            # r.d = r.e


    i = fields.Integer()
    j = fields.Integer(compute='_j',store=True)
    k = fields.Integer()#compute='_k',store=True
    h = fields.Integer(store=True)#compute='_h'
    # {tp.sale.order.i: {None: {tp.sale.order.j, tp.sale.order.k, tp.sale.order.h}}, tp.sale.order.j: {None: {tp.sale.order.k}}, tp.sale.order.name: {None: {tp.sale.order.display_name}}, tp.sale.order.write_date: {None: {tp.sale.order.__last_update}}, tp.sale.order.create_date: {None: {tp.sale.order.__last_update}}}
    # {tp.sale.order.i: {None: {tp.sale.order.k, tp.sale.order.j}}, tp.sale.order.k: {None: {tp.sale.order.k, tp.sale.order.j}},
    
    #truowngf hop co compute='_k'
    # field tp.sale.order.j path (tp.sale.order.k,)
    # field tp.sale.order.j path (tp.sale.order.customer_id, res.partner.user_id)
    # field tp.sale.order.j path (tp.sale.order.j,)
    # field tp.sale.order.j path (tp.sale.order.customer_id, res.partner.user_id, res.users.name)
    # field tp.sale.order.j path (tp.sale.order.customer_id,)
    # field tp.sale.order.j path (tp.sale.order.customer_id, res.partner.user_id)
    # field tp.sale.order.j path (tp.sale.order.customer_id,)
    # field tp.sale.order.j path (tp.sale.order.i,)
    
    #truong hop khong co 
    # field tp.sale.order.j path (tp.sale.order.customer_id, res.partner.user_id)
    # field tp.sale.order.j path (tp.sale.order.i,)
    # field tp.sale.order.j path (tp.sale.order.k,)
    # field tp.sale.order.j path (tp.sale.order.customer_id,)
    @api.depends('i','k','customer_id.user_id')
    def _j(self):
        print ('compute j', [k for k in self.env._protected])
        for r in self:
            r.j = r.i

    @api.depends('j','customer_id.user_id.name')
    def _k(self):
        print ('compute k', [k for k in self.env._protected])
        for r in self:
            r.k = r.j

    # @api.depends('i')
    # def _h(self):
    #     print ('compute h', [k for k in self.env._protected])
    #     for r in self:
    #         r.h = r.k

    def test(self):
        # raise UserError(_('This addon is already installed on your system'))
        raise UserError(_('This addon is already installed on your system kaka'))





