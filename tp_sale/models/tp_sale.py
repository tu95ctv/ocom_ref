# -*- coding: utf-8 -*-
from locale import currency
from odoo import models, fields, api, _, tools
from odoo.exceptions import UserError
from time import sleep
from odoo.tools import config
from datetime import date
# from odoo.addons.queue_job.job import job #khoong hieu sao phien bang nay bi @job

import logging
_logger = logging.getLogger(__name__)
import threading
import inspect
from odoo.tools import ormcache, ormcache_context
# class User(models.Model):
#     _inherit = 'res.users' #tên bàng tp_sale

#     new_field = fields.Char()

class Contact(models.Model):
    _inherit = 'res.partner' #tên bàng tp_sale
    
    def print_abc(self):
        print ('abc', config['data_dir'],'haha',config.filestore('o141'))
class SaleParent(models.Model):
    _name = 'tp.sale.order.parent' #tên bàng tp_sale

    xyz = fields.Char()


class Sale(models.Model):
    _name = 'tp.sale.order' #tên bàng tp_sale
    _description = 'TP sale'
    # _inherit=['xmlidab.xmlidab']
    # _inherit = ['mail.thread.cc']

    a2 = fields.Char()
    a3 = fields.Char()
    compute_g_field = fields.Char(groups='tp_sale.group_user_tp_sale', compute='_compute_compute_g_field', store=True)
    tr_field = fields.Char()
    @api.depends('tr_field')
    def _compute_compute_g_field(self):
        print ('*self.env.user', self.env.user)
        print ('1111111111111')
        for r in self:
            r.compute_g_field = r.tr_field

    g_field = fields.Char(groups='tp_sale.group_user_tp_sale')
    # _inherits = {'tp.sale.order.parent': 'tp_sale_parent_id'}
    amount = fields.Float(compute='_compute_amount', store=True)
    # amount = fields.Float()
    line_ids = fields.One2many('tp.sale.order.line', 'order_id', copy=True)
    dup_line_ids = fields.One2many('tp.sale.order.line', 'order_id', copy=True)
    len_lines = fields.Integer(compute='_compute_len_line', store=True)
    # ref_line_ids = fields.One2many('tp.sale.order.line', 'res_id')
    image_test = fields.Binary(attachment=False)
    name = fields.Char(default='anh nhơ me')
    customer_id = fields.Many2one('res.partner', auto_join=True)
    order_date = fields.Date()  
    number = fields.Float(digits=(6,2))
    a1 = fields.Integer()
    b1 = fields.Integer(compute='_compute_b1', store=True, string='b1' )
    c1 = fields.Integer(compute='_compute_c1', store=True, readonly=False )
    d1 = fields.Char(compute='_compute_d1', store=True)
    e = fields.Integer()
    g3 = fields.Integer()
    attachment_ids = fields.One2many('ir.attachment','res_id')
    line_id = fields.Many2one('tp.sale.order.line')
    name_line = fields.Char(related='line_id.name', store=True)
    m2m_line_ids = fields.Many2many('tp.sale.order.line','so_sol_rel','so_id','sol_id')
    m2m_a_line_ids = fields.Many2many('tp.sale.order.line', store=True)
    number2 = fields.Integer()
    dt = fields.Date()
    nr = fields.Integer('Number required', required=True, default=1)
    cr = fields.Char('Char required', required=True,default=1)
    gr = fields.Char(groups='tp_sale.group_user_tp_sale')
    e = fields.Integer()
    i = fields.Integer()
    k = fields.Integer()#compute='_k',store=True
    h = fields.Integer(store=True)#compute='_h'
    customer_ids = fields.Many2many('res.partner')
    currency_id = fields.Many2one('res.currency', default = lambda self: self.env.user.company_id.currency_id)
    m1 = fields.Monetary()
    
    def see_field_triggers(self):
        p = self.pool
        ft = p.field_triggers
        T = self.env['tp.sale.order']
        fs = T._fields
        fd1 = fs['d1']
        fd1.resolve_depends(p)
        fd1_trigger = ft[fd1]


        p = self.pool
        ft = p.field_triggers
        T = self.env['tp.sale.order']
        fs = T._fields
        fd1 = fs['customer_id']
        fd1_trigger = ft[fd1]

        p = self.pool
        ft = p.field_triggers
        P = self.env['res.partner']
        Pfs=P._fields
        Pname = Pfs['name']
        fd1_trigger = ft[Pname]


    @api.depends('customer_id.name')
    def _compute_d1(self):
        for r in self:
            r.d1 = r.customer_id.id

    def assign4(self):
        self.env.ref('tp_sale.tp_sale_order_1').with_user(2).a1 = 2

    @api.depends('line_ids.price','m2m_a_line_ids')
    def _compute_amount(self):
        for rec in self:
            rec.amount = sum(rec.line_ids.mapped('price_unit'))

    @api.depends('line_ids','line_ids.product_id')
    def _compute_len_line(self):
        for r in self:
            r.len_lines = len(r.line_ids)

    
    # def _set_a1(self):
    #     for r in self:
    #         r.a1 = r.b1/2

    @api.depends('a1')
    def _compute_b1(self):
        print ('_compute_b1')
        for r in self:
            r.b1 = 2*r.a1

    @api.depends('b1')
    def _compute_c1(self):
        for r in self:
            r.c1 = 2*r.b1


    @tools.ormcache('self.env.uid', 'self.env.su')
    def test_cache(self):
        print ("test cache 2")
        return 2
    @api.onchange('customer_id')
    def _oc_customer_id(self):
        self.number = self.customer_id.id
    # @api.depends('i','k','customer_id.user_id')
    # def _j(self):
    #     print ('compute j', [k for k in self.env._protected])
    #     for r in self:
    #         r.j = r.i

    # @api.depends('j','customer_id.user_id.name')
    # def _k(self):
    #     print ('compute k', [k for k in self.env._protected])
    #     for r in self:
    #         r.k = r.j

    
        
    # def unlink(self):
    #     res = self.unlink()
    #     return res



    # @api.onchange('a')
    # def _onchange_a(self):
    #     print ('kakak')
    #     self.c = 5 + self.a
    #     self.line_ids = \
    #     [(0, 0, {
    #             'product_id': 1,
    #             'line1_ids': [(4, 1),
    #                 (0, 0, {
    #                     'product_id': 3,
    #                     'name': 'line1',
    #                     'line2_ids': [(0, 0, {
    #                         'product_id': 3,
    #                         'name': 'line2'
    #                     })]
    #                 })
    #             ]

    #         })]



    def test(self):
        # raise UserError(_('This addon is already installed on your system'))
        raise UserError(_('This addon is already installed on your system kaka'))

    def action_test_for_debug(self):
        # self.write({'line_ids':[(0,0,{'product_id':1})]})
        # initial_values = {'name': 'anh nhơ me', 'image_test': False, '__last_update': '2022-02-05 08:24:40', 'customer_id': False, 'number': 0, 'order_date': False, 'a': False, 'b': 12, 'c': 6, 'line_ids': [[1, 66, {'name': False, 'product_id': 3, 'qty': 7, 'price_unit': 0, 'price': 0}]], 'm2m_line_ids': [[6, False, []]], 'attachment_ids': [], 'id': 61}
        initial_values = {'line_ids': [[1, 66, {'name': False, 'product_id': 3, 'qty': 7}]]}

        record = self.new(initial_values, origin=self)
        print (record.line_ids.qty)

    def action_test_create_for_debug(self):
        # self.create({'name':1, 'line_ids':[(0,0,{'product_id':1})]})  
        self.search([], limit=1).line_ids = [(0,0,{'product_id':1}),(0,0,{'product_id':1})]

    
    def action_test_create_m2m_for_debug(self):
        self.create({'name':1, 'm2m_line_ids':[(0,0,{'product_id':1})]})


   
    # @job # khoong hieu sao phien bang nay bi @job
    def create_queue(self, vals):
        print ("self._context.get('create')", self._context.get('create'))
        print ("self.env.user", self.env.user)
        if self._context.get('create'):
            self.create(vals)

    def test_queue(self):
        print ("self._context.get('create') 1", self._context.get('create'))
        self.with_delay().create_queue({'name': 'test queue'})

    # def test_new(self):
    #     values = {'name': 'anh nhơ me', 'image_test': False, '__last_update': '2022-02-26 06:49:21', 'customer_id': False, 'number': 0, 'amount': 11, 'order_date': False, 'a': False, 'b1': 62, 'c': 0, 'line_ids': [[4, 3, False], [4, 4, False], [0, 'virtual_817', {'product_id': 45, 'price_unit': 8, 'price': 0, 'qty': 0, 'line1_ids': [[6, False, []]]}]], 'm2m_line_ids': [[6, False, []]], 'attachment_ids': []}
    #     s = self.env['tp.sale.order'].new(values)

    def test_new(self):
        values = {'name': 'anh nhơ me'}
        s = self.env['tp.sale.order'].new(values)
        value = s.a
        print ('value', value)

    def action_test_create1(self):
        print ('ndt',self._context)

    def assign1(self):
        self.env.ref('tp_sale.tp_sale_order_1').line_ids = self.env.ref('tp_sale.tp_sale_line_1')

    def assign2(self):
        self.env.ref('tp_sale.tp_sale_order_1').line_ids = False

    def assign3(self):
        self.env.ref('tp_sale.tp_sale_order_1').line_ids = [(0,0,{'product_id':self.env.ref('tp_sale.product_product_p1_1').id})]

    def assign4(self):
        self.env.ref('tp_sale.tp_sale_order_1').line_ids = [(0,0,{'product_id':self.env.ref('tp_sale.product_product_p1_1').id}),(5,)]

    def assign5(self):
        self.env.ref('tp_sale.tp_sale_order_1').line_ids = [(5,)]

    def assign6(self):
        self.env.ref('tp_sale.tp_sale_order_1').line_ids = [(5,),(0,0,{'product_id':self.env.ref('tp_sale.product_product_p1_1').id})]

    def assign7(self):
        self.env.ref('tp_sale.tp_sale_order_1').line_ids = self.line_ids.new({'product_id':self.env.ref('tp_sale.product_product_p1_1').id})



    # def assign1(self):
    #     self.env.ref('tp_sale.tp_sale_order_1').with_user(2).g_field = 'xyz'

    # def assign2(self):
    #     self.env.ref('tp_sale.tp_sale_order_1').customer_id = self.env.user.partner_id

    # def assign3(self):
    #     self.env.ref('tp_sale.tp_sale_order_1').with_user(2).tr_field = 'xyz3'

    def read1(self):
        print (self.env.ref('tp_sale.tp_sale_order_1').customer_id)

    def read_g_field(self):
        print ('self.env.user', self.env.user)
        print (self.env.ref('tp_sale.tp_sale_order_1').with_user(2).g_field)

    def read_g_field(self):
        print ('self.env.user', self.env.user)
        print (self.env.ref('tp_sale.tp_sale_order_1').with_user(2).g_field)

   
    def cronjob_test_active_toggle_line(self):
        self.env.ref('tp_sale.tp_sale_line_1').toggle_active()

    def cronjob_read_active_test_false(self):
        print (self.env.ref('tp_sale.tp_sale_order_1').with_context(active_test=False).line_ids)

    def cronjob_read_active_test_false_after(self):
        print (self.env.ref('tp_sale.tp_sale_order_1').line_ids.with_context(active_test=False))

    def create4(self):
        self.create({
            'name':'m1',
            'm1':1.22222
        })
        

    # @api.onchange('number')
    # def _onchange_number(self):
    #     print ('self.id', self.id, bool(self.id),'self.ids',self.ids, 'self.m2m_line_ids',self.m2m_line_ids,self.m2m_line_ids.ids)
    #     print ('self.b', self.b)
    #     if self.number:
    #         rs = self.env['tp.sale.order.line'].search([], limit=self.number, order='id desc')
    #         self.line_ids = rs
    #         self.line_ids = [(0,0,{'product_id':1, 'qty':100})]
    #         self.line_ids = [(1,1,{'product_id':1, 'qty':1000})]
    

    

    # @api.model
    # @ormcache('str(views)','str(options)')
    # def load_views(self, views, options=None):
    #     print ('*load_views*'*100)
    #     rs = super(Sale, self).load_views(views,options)
    #     return rs
    #     # options = options or {}
    #     # result = {}

    #     # toolbar = options.get('toolbar')
    #     # result['fields_views'] = {
    #     #     v_type: self.fields_view_get(v_id, v_type if v_type != 'list' else 'tree',
    #     #                                  toolbar=toolbar if v_type != 'search' else False)
    #     #     for [v_id, v_type] in views
    #     # }
    #     # result['fields'] = self.fields_get()

    #     # if options.get('load_filters'):
    #     #     result['filters'] = self.env['ir.filters'].get_filters(self._name, options.get('action_id'))


    #     # return result

    


