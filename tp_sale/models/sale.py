# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from time import sleep
from odoo.tools import config
from datetime import date
import logging
_logger = logging.getLogger(__name__)
import threading

# class User(models.Model):
#     _inherit = 'res.users' #tên bàng tp_sale

#     new_field = fields.Char()

class Contact(models.Model):
    _inherit = 'res.partner' #tên bàng tp_sale
    
    def print_abc(self):
        print ('abc', config['data_dir'],'haha',config.filestore('o141'))


class SaleParent(models.Model):
    _name = 'tp.sale.parent' #tên bàng tp_sale

    xyz = fields.Char()


class Sale(models.Model):
    _name = 'tp.sale' #tên bàng tp_sale
    _description = 'TP sale'
    # _inherits = {'tp.sale.parent': 'tp_sale_parent_id'}

    image_test = fields.Binary(attachment=False)
    image_test_a = fields.Binary()
    name = fields.Char(x=1)
    customer_id = fields.Many2one('res.partner', domain=[('id','in',(3,4))])
    ### field one2many này hơi mới so với framework khác
    # One2many trường không có cột trong database
    # Nó liên kết tới 1 bảng khác, bảng đó có 1 cột khóa ngoại liên kết về bảng này
    # ở đây là bảng tp.sale.line liên kết tới bảng tp.sale bằng khóa ngoại sale_id
    sale_line_ids = fields.One2many('tp.sale.line', 'sale_id')
    amount = fields.Float(compute='_compute_amount', store=True)
    order_date = fields.Date()  
    sale_line_test_id = fields.Many2one()
    number = fields.Integer()
    order_date_input = fields.Date()
    customer_ids = fields.Many2many('res.partner', 'tp_sale_res_partner_relation', 'tp_sale_id', 'customer_id')
    
    def create_tp_sale_raise_tp_sale_line(self):
        data = {
            'name': 'test1',
            'sale_line_ids': [(0,0,{'qty':2})]
        }
        self.create([data])

    def test_abc(self):
        
        print ('abc')

    def test_abc1(self):
        try:
            self.create_crm_lead_one()
        except:
            pass
    
    def create_crm_lead_one_with_day_month(self,month, day):
        print ('*create_crm_lead_one_with_day_month*')
        C = self.env['crm.lead']
        last_contact_date = date(2021,month,day)
        C.create({'name': 'test', 
            'type':'opportunity',
            'deal_ref': False, 
            'last_contact_date':last_contact_date})

      
    def create_crm_lead_one(self, thread_i):
        C = self.env['crm.lead']
        C.create({'name': 'test', 'deal_ref': False})


    


    def create_crm_lead(self, thread_i):
        print ('bắt đầu tạo 1-1000 crm.lead')
        for i in range(20):
            month=i%5 or 5
            day = i%28 or 28
            self.create_crm_lead_one_with_day_month(month, day)
    
    def write_crm_lead(self,thread_i=0):
        C = self.env['crm.lead']
        limit = 2
        offset = thread_i*limit
        crms = C.search([], limit=limit, offset=offset)
        for count, c in enumerate(crms):
            print (c)
            deal_ref = offset + count
            c.write({'deal_ref':deal_ref})


    def count_1_to_n(self):
        for i in range(20):
            print (i)
            sleep(1)

    def test_queue(self):
        for thread_i in range(10):
            print ('thread_i', thread_i)
            self.with_delay().write_crm_lead(thread_i)

    def test_queue_create(self):
        print ('')
        for thread_i in range(20):
            print ('thread_i', thread_i)
            self.with_delay().create_crm_lead(thread_i)
            
            


    @api.depends('sale_line_ids.price')
    def _compute_amount(self):
        for rec in self:
            rec.amount = sum(rec.sale_line_ids.mapped('price'))

    def test_loi(self):
        print ('test loi')
        with self.pool.cursor() as cr:
            cr.autocommit(True)
            for i in range(6):
                self.number +=1
                sleep(1)
                print('self.number', self.number)

    def print_out_in_date(self):
        # rs = self.env['tp.sale'].search([('order_date','=', self.order_date_input),('customer_id','=', 1)])
        # # print (rs)
        self.write({'number': 2 })
        # self.customer_id = 1# test dòng này ở đây


        # try:
        #     with self.env.cr.savepoint():
        #         self.customer_id = 1 # và dòng này ở đây có khác nhau gì
        #         1/0
        # except:
        #     pass

        try:
            self.customer_id = 2 # và dòng này ở đây có khác nhau gì
            1/0
        except:
            pass

    def test(self):
        # in ra tên khách hàng của tp.sale có id là 3, bài tập về relation nha
        tp_sale_3 = self.env['tp.sale'].browse([3])
        print (tp_sale_3.customer_id.name)

        # search những đơn hàng  của khách hàng có tên là 'abc'

        rs = self.env['tp.sale'].search([('customer_id.name','=','abc')])
        _logger.info('Hóa đơn của khách abc: %s'%rs)


        # search những đơn hàng  của khách hàng đến từ Hà Nội

        rs = self.env['tp.sale'].search([('customer_id.state_id.name','=','Hà Nội')])
        _logger.info('hóa đơn từ Hà Nội %s'%rs)


# class TPsaleInherit(models.Model):
#     _inherit = 'tp.sale'

#     inherit_test = fields.Char()



# class TPSale2(models.Model):
#     _inherit = 'tp.sale'

#     tpsale2 = fields.Char()
   


    
class SaleLineTest(models.Model):
    _name = 'tp.sale.line.test'
    _description = 'TP sale'

    name = fields.Char()

    # def create(self, vals_list):
    #     raise ValueError('akakaka')



