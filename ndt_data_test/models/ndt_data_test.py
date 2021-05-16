# -*- coding: utf-8 -*-
from odoo import models, fields, api
import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round
from time import sleep
xmlidmodule = 'ndt_data_test1'
from time import sleep
import logging
import threading


from odoo import api, SUPERUSER_ID

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
    tl_ids = fields.Many2many('test.line')
    type = fields.Selection([('trobz_wage', 'trobz_wage'),
                             ('sale_order', 'sale_order')], default='trobz_wage')
    # stt = fields.Char(default=1, readonly=1)
    domain = fields.Char(default=[])
    name = fields.Char(translate=True)
    now_stt = fields.Char(compute='_compute_now_stt')
    auto_increase_stt = fields.Boolean(default=True)
    is_validate_invoice = fields.Boolean(default=True)
    is_promote_sol = fields.Boolean(default=True)

    input_date = fields.Date(
        default=lambda self: fields.Date.context_today(self))
    is_input_date = fields.Boolean(default=True)
    is_last_month = fields.Boolean()
    is_last_year = fields.Boolean(default=True)
    input_text = fields.Integer()
    t2 = fields.Char()
    ############# Create so ################



    def test(self):
        print ('akdfkdsjflkdf dklf')
        raise UserError('akakak')
        self.rs = 1
        self.input_text = 2
        return

    # @api.multi
    def write(self, vals):
        print ('write....................', vals)
        super().write(vals)

    def _write(self, vals):
        print ('_write....................', vals)
        super()._write(vals)

    def test_update_no_wait(self,t):
        cr = self._cr
        cr = self.pool.cursor()
        query = "select id from hr_employee where id = %s  FOR UPDATE"
        params = (1,)
        try:
            cr.execute(query, params)
            rs = cr.fetchone()
        except Exception as e:
            raise ValueError('đạu xanh cái gì bị ', t, e)
        print ('************rs o test %s**********'%t,rs)
        count = 6
        while count:
            print ('count trong',t,count)
            sleep(1)
            count -=1

    @return_this_view_wrap
    def test3(self):
        print ('trong test 3', self._cr)
        self.test_update_no_wait(3)
        
    @return_this_view_wrap
    def test4(self):
        print ('trong test 4',self._cr)
        self.test_update_no_wait(4)

  

    @return_this_view_wrap
    def test2(self):
        self.test_em2()
        # self.test_abc()

    def fetch_cron(self):
        count = 60
        while count:
            sleep(1)
            count -=1
            _logger.warning ('****trong cron job**** count là: %s'%count)


    def test_server(self):
        print ('^^^^^^^^^^^^^^^^trong test server^^^^^^^^^^^^^^^^^^',threading.current_thread())
        pass

    

    

        
        
    def test_abc(self):
        rs = self.pool.registries
        len_r = len(rs)

        k = [(i,r) for i,r in rs.d.items()]
        print ('***len_r***', len_r)
        raise UserError('%s-%s'%(len_r,k))
        # print (abc)

    # có commit
    # def test_em1(self):
    #     with self.pool.cursor() as cr:
    #         cr.autocommit(True)
    #         env = api.Environment(cr, SUPERUSER_ID, {})
    #         self = self.with_env(env)
    #         print ('***********vào test 1********',threading.current_thread())
    #         first_employee = self.env['hr.employee'].search([],order='id asc', limit=1)
    #         test_number = first_employee.test_number
    #         for i in range(6):
    #             first_employee.test_number +=1
    #             print ('***first_employee.test_number1***',
    #             first_employee.test_number)
    #             sleep(1)

    def test_em1(self):
      
        print ('***********vào test 1********',threading.current_thread())
        first_employee = self.env['hr.employee'].search([],order='id asc', limit=1)
        test_number = first_employee.test_number
        for i in range(6):
            first_employee.test_number +=1
            print ('***first_employee.test_number1***',
            first_employee.test_number, threading.current_thread())
            sleep(1)
        print ('kết thúc 111')


    def test_em2(self):
        print ('*******vào test 2**********', threading.current_thread())
        cr = self.env.cr
        first_employee = self.env['hr.employee'].search([],order='id asc', limit=1)
        test_number = first_employee.test_number
        print ('***test_number ở 2**', test_number,' lấy first_employee.name', first_employee.name,'threading.current_thread()',threading.current_thread() )
        for i in range(10):
            sleep(1)
        print ('ở 2 kết thúc chờ 10 giây...')
        for i in range(6):
            first_employee.test_number +=1
            print ('***first_employee.test_number ở test number 2 :%s***'%first_employee.test_number,threading.current_thread()
            )
            sleep(1)


    # def test_em1(self):
    #     with self.pool.cursor() as cr:
    #         cr.autocommit(True)
    #         env = api.Environment(cr, SUPERUSER_ID, {})
    #         self = self.with_env(env)

    #         print ('***********vào test 1********',threading.current_thread())
    #         first_employee = self.env['hr.employee'].search([],order='id asc', limit=1)
    #         for i in range(6):
    #             first_employee.test_number = first_employee.test_number +  1
    #             print ('***first_employee.test_number1***',
    #             # 'self.env.cr**',self.env.cr,'cache',
    #             # self.env.cache,self.env.envs,
    #             # 'self.env.registry',self.env.registry,
    #             # 'threading.current_thread()',threading.current_thread(),
    #             'test_number', first_employee.test_number, threading.current_thread())
    #             sleep(1)
    #         # self.env['hr.employee'].flush()

    # def test_em2(self):
    #     print ('***********vào test 2********',threading.current_thread())
    #     cr = self.env.cr
    #     first_employee = self.env['hr.employee'].search([],order='id asc', limit=1)
    #     for i in range(6):
    #         first_employee.test_number2 = first_employee.test_number2 +  1
    #         # _logger.warning ('***first_employee.test_number :%s***',
    #         # first_employee.test_number2
    #         # )
    #         print ('***first_employee.test_number2 :%s***'%first_employee.test_number2,threading.current_thread()
    #         )
    #         sleep(1)







    @return_this_view_wrap
    def testx(self):
        CT = self.env['test.model']
        c = CT.search([], limit=1)
        if not c:
            c = c.create({'name_test':'abc'})
        print('*******begin ở test3*******')
        # c.wage = self.input_text
        print('***tìm hiểu cache')
        name_test_field = c._fields['name_test']

        try:
            name_test_cache = c.env.cache._data.get(name_test_field).get(c.id)
            print('***name_test_cache** 1', name_test_cache)
            print('***c.env.cache._data***1', c.env.cache._data)
        except:
            pass
        c.name_test = self.input_text

        try:
            name_test_cache = c.env.cache._data.get(name_test_field).get(c.id)
            print('***name_test_cache** 2', name_test_cache)
            print('***c.env.cache._data***2', c.env.cache._data)
        except:
            pass
        # print ('kết thúc nè buồn quá')
        # c.wage = int(self.input_text) + 2
        # print ('cộng thêm')
        # c.wage +=1
        # c.name = 'abc'
        # c.write({
        #     'wage':self.input_text
        # })

    @return_this_view_wrap
    def create_data_test(self):
        if self.type == 'trobz_wage':
            self._create_trobz_wage()
        if self.type == 'sale_order':
            self._create_data_test()

    def _set_trobz_env(self):
        DP = self.env['hr.department']
        JOB = self.env['hr.job']
        EM = self.env['hr.employee']
        CT = self.env['hr.contract']
        PWH = self.env['payroll.wage.history']
        wage1 = 10.15
        wage2 = 11.25
        contract_name = 'Hợp đồng lập trình 1'
        return {'EM': EM, 'wage1': wage1, 'wage2': wage2, 'contract_name': contract_name, 'JOB': JOB}
        # self.test_env.update( )

    def _create_trobz_wage(self, xmlidmodule=xmlidmodule):
        test_env = self._set_trobz_env()
        self = self.with_context(te=test_env)
        rs = []
        rt = self._create_trobz_wage_1(xmlidmodule)
        rs.append(rt)

        rt = self._create_trobz_wage_2(xmlidmodule)
        rs.append(rt)

        rt = self._create_trobz_wage_3(xmlidmodule)
        rs.append(rt)
        self.rs = rs

    def _create_trobz_wage_2(self, xmlidmodule=xmlidmodule):
        te = self._context['te']
        DP = self.env['hr.department']
        # JOB = self.env['hr.job']
        JOB = te['JOB']
        # EM = self.env['hr.employee']
        EM = te['EM']
        CT = self.env['hr.contract']
        PWH = self.env['payroll.wage.history']
        wage1 = 10.15
        wage2 = 11.25
        contract_name = 'Hợp đồng lập trình 1'

        # department_id = DP.search([],limit=1)
        job_id = JOB.search([], limit=1)
        employee_id = EM.search([], limit=1)

        contract_id = self.xmlid_to_object_fix_module(
            contract_name, xmlidmodule)
        contract_id.write({'wage': wage2})

        pwh = PWH.search([('contract_id', '=', contract_id.id)],
                         order='id desc', limit=1)

        rt = pwh.difference == float_round(wage2 - wage1, 2)
        print('pwh.revision', pwh.revision)
        print('trả về trong _create_trobz_wage_2', rt)
        return [rt, pwh]

    def _create_trobz_wage_1(self, xmlidmodule=xmlidmodule):

        DP = self.env['hr.department']
        JOB = self.env['hr.job']
        EM = self.env['hr.employee']
        CT = self.env['hr.contract']
        PWH = self.env['payroll.wage.history']

        # department_id = DP.search([],limit=1)
        job_id = JOB.search([], limit=1)
        employee_id = EM.search([], limit=1)
        wage1 = 10.15
        wage2 = 11.25
        contract_name = 'Hợp đồng lập trình 1'

        #######tao department####
        department_name = 'Lập Trình'
        rs = []
        vals = {
            'name': department_name,
        }
        model = 'hr.department'
        deparment_id = self.create_record_with_xmlid1(
            department_name, model, vals, xmlidmodule)
        print('***deparment_id***', deparment_id)
        rs.append(deparment_id)

        #######tao Employee####
        name = 'Nguyễn Văn B'
        rs = []
        vals = {
            'department_id': deparment_id.id,
            'name': name,
        }
        model = 'hr.employee'
        employee_id = self.create_record_with_xmlid1(
            name, model, vals, xmlidmodule)
        rs.append(employee_id)

        ###tao contract#####3

        vals = {
            'name': contract_name,
            'department_id': deparment_id.id,
            'job_id': job_id.id,
            'employee_id': employee_id.id,
            'wage': wage1,

        }
        model = 'hr.contract'
        contract_id = self.create_record_with_xmlid1(
            contract_name, model, vals, xmlidmodule)
        rs.append(contract_id)
        #########3
        return rs

    def _create_trobz_wage_3(self, xmlidmodule=xmlidmodule):

        DP = self.env['hr.department']
        JOB = self.env['hr.job']
        EM = self.env['hr.employee']
        CT = self.env['hr.contract']
        PWH = self.env['payroll.wage.history']

        # department_id = DP.search([],limit=1)
        job_id = JOB.search([], limit=1)
        employee_id = EM.search([], limit=1)
        wage1 = 10.15
        wage2 = 11.25
        contract_name = 'Hợp đồng lập trình'
        wage3 = 20

        #######tao department####
        department_name = 'Lập Trình'
        rs = []
        vals = {
            'name': department_name,
        }
        model = 'hr.department'
        deparment_id = self.create_record_with_xmlid1(
            department_name, model, vals, xmlidmodule)
        print('***deparment_id***', deparment_id)
        rs.append(deparment_id)
        # deparment_id = self.xmlid_to_object_fix_module(department_name, xmlidmodule)
        #######tao department####

        #######tao Employee####
        name = 'Nguyễn Văn A'
        rs = []
        vals = {
            'department_id': deparment_id.id,
            'name': name,
        }
        model = 'hr.employee'
        employee_id = self.create_record_with_xmlid1(
            name, model, vals, xmlidmodule)
        rs.append(employee_id)
        # deparment_id = self.xmlid_to_object_fix_module(department_name, xmlidmodule)
        #######tao department####

        ###tao contract#####3

        vals = {
            'name': name,
            'department_id': deparment_id.id,
            'job_id': job_id.id,
            'employee_id': employee_id.id,
            'wage': wage3,

        }
        model = 'hr.contract'
        contract_id = self.create_record_with_xmlid1(
            contract_name, model, vals, xmlidmodule)
        rs.append(contract_id)
        return rs

    def xmlid_to_object_fix_module(self, name, xmlidmodule=xmlidmodule):
        name = re.sub('\s+', '_', name)
        xmlid = xmlidmodule + '.' + name
        I = self.env['ir.model.data']
        obj = I.xmlid_to_object(xmlid)
        return obj

    def create_record_with_xmlid1(self, name, model, vals, xmlidmodule=xmlidmodule):
        name = re.sub('\s+', '_', name)
        I = self.env['ir.model.data']

        xml_id = xmlidmodule + '.' + name
        contract_id = I.xmlid_to_object(xml_id)
        if contract_id:  # update
            contract_id.write(vals)
        else:
            contract_id = self.env[model].create(vals)
            self.env['ir.model.data'].create({
                'name': name,
                'model': model,
                'module': xmlidmodule,
                'res_id': contract_id.id,
            })
        return contract_id

    # @return_this_view_wrap
    # def test2(self):
    #     CT = self.env['hr.contract']
    #     c = CT.search([], limit=1)

    #     c.write({
    #         'notes': 1, 'history_ids': [(1, c.history_ids[0].id, {'current_wage': self.input_text})]
    #     })

    @return_this_view_wrap
    def test1(self):
        print('*********self.input_text*******', self.input_text)
        w = self.env['payroll.wage.history'].search([], limit=1)
        # w.write({'previous_wage':11})
        w.write({'previous_wage': self.input_text})

    def _create_data_test(self):
        rs = []
        self.increase_stt()

        # so = self.create_so()
        # rs.append(so)

        # rt = self.create_sol()
        # rs.append(rt)

        # so = self.create_so_last_year()

        if self.is_input_date:
            so = self.create_common_so()
            # rt = self._invoice_create(so)
            self.validate_delivery(so)  # sao mấy cái kia ko chơi vậy lun
            rs.append(so)
            #last đate
            so = self.create_so_last_date()
            # rt = self._invoice_create(so)
            # self.validate_delivery(so) # sao mấy cái kia ko chơi vậy lun
            rs.append(so)

        if self.is_last_month:
            so = self.create_so_last_month()
            # rt = self._invoice_create(so)

            # so = self.create_so_last_month_and_1_day()
            # rt = self._invoice_create(so)

            so = self.create_so_last_2_month()
            # rt = self._invoice_create(so)

            # self.validate_delivery(so)#
            rs.append(so)

        if self.is_last_year:
            so = self.create_so_last_year()
            # rt = self._invoice_create(so)
            rs.append(so)

        self.rs = rs

    def create_common_so(self, suffix_xml_before='curent', date_order=None, so_kh=1):
        input_date = self.input_date
        if not date_order:
            date_order = input_date
        suffix_xml_after = date_order
        suffix_xml = '%s_%s' % (suffix_xml_before, suffix_xml_after)
        # 'confirmation_date':confirmation_date,
        # 'validity_date':confirmation_date,
        so = self.create_so(suffix_xml=suffix_xml,
                            date_order=date_order, so_kh=so_kh)
        sol = self.create_sol(order_id=so, suffix_xml=suffix_xml)
        self._invoice_create(so)
        return so

    def create_so_last_date(self):
        input_date = fields.Date.from_string(self.input_date)
        date_order = input_date - relativedelta(days=1)
        suffix_xml_before = 'last_date'
        so = self.create_common_so(
            suffix_xml_before=suffix_xml_before, date_order=date_order, so_kh=2)
        return so

    def create_so_last_year(self):
        input_date = fields.Date.from_string(self.input_date)
        date_order = input_date - relativedelta(years=1)
        suffix_xml_before = 'last_year'
        so = self.create_common_so(
            suffix_xml_before=suffix_xml_before, date_order=date_order)
        return so

    def create_so_last_month(self):
        input_date = fields.Date.from_string(self.input_date)
        date_order = input_date - relativedelta(months=1)
        suffix_xml_before = 'last_month'
        so = self.create_common_so(
            suffix_xml_before=suffix_xml_before, date_order=date_order)
        return so

    def create_so_last_month_and_1_day(self):
        input_date = fields.Date.from_string(self.input_date)
        date_order = input_date - relativedelta(months=1, days=-1)
        suffix_xml_before = 'last_month_and_1day'
        so = self.create_common_so(
            suffix_xml_before=suffix_xml_before, date_order=date_order, so_kh=2)
        return so

    def create_so_last_2_month(self):
        input_date = fields.Date.from_string(self.input_date)
        date_order = input_date - relativedelta(months=2)
        suffix_xml_before = 'last_2_month'
        so = self.create_common_so(
            suffix_xml_before=suffix_xml_before, date_order=date_order)
        return so

    def create_so(self, suffix_xml='', date_order=False, so_kh=1):
        stt = self.stt
        name = 'ndt_so_%s_%s' % (suffix_xml, stt)
        ref = self.env.ref
        vals = {
            'partner_id': ref('ndt_data_testf.kh_%s' % so_kh).id,
            'date_order': date_order,
            'confirmation_date': date_order,
            'validity_date': date_order,
        }
        model = 'sale.order'
        rt = self.create_record_with_xmlid(name, model, vals)
        so = ref('ndt_data_testf.' + name)
        # rt = sef.env['sale.order'].browse(rt[0])
        return so

    def create_sol(self, order_id=None, suffix_xml='', is_create_two=False):
        ref = self.env.ref
        stt = self.stt
        order_id = order_id.id

        name = 'ndt_sol_%s_%s' % (suffix_xml, stt)
        vals = {
            'order_id': order_id,
            'product_id': ref('ndt_data_testf.sp_1').id,
            'product_uom_qty': 10,
        }
        model = 'sale.order.line'
        rt = self.create_record_with_xmlid(name, model, vals)

        if is_create_two:
            name = 'ndt_sol2_%s_%s' % (suffix_xml, stt)
            ref = self.env.ref
            vals = {
                'order_id': order_id,
                'product_id': ref('ndt_data_testf.sp_1').id,
                'product_uom_qty': 10,
            }
            model = 'sale.order.line'
            rt = self.create_record_with_xmlid(name, model, vals)

        if self.is_promote_sol:
            #giảm giá:
            name = 'ndt_sol_gg%s_%s' % (suffix_xml, stt)
            vals = {
                'order_id': order_id,
                'product_id': ref('ndt_data_testf.gg_1').id,
                'product_uom_qty': 10,
            }

            rt_gg = self.create_record_with_xmlid(name, model, vals)

        return rt

    def _invoice_create(self, sale_order=None, open_invoice=True):
        sale_order.action_confirm()
        sale_order.confirmation_date = sale_order.date_order
        rt = sale_order.with_context(
            default_date_invoice=sale_order.date_order).action_invoice_create()
        # rt.date_invoice =
        inv_obj = self.env['account.invoice'].browse(rt[0])
        if not open_invoice:
            open_invoice = self.is_validate_invoice
        if open_invoice:
            inv_obj.action_invoice_open()
        return inv_obj

    def validate_delivery(self, sale_order):
        picking_ids = sale_order.picking_ids
        picking_ids.scheduled_date = sale_order.date_order
        for ml in picking_ids.move_lines:
            ml.quantity_done = 10
        picking_ids.with_context(
            default_date=sale_order.date_order).button_validate()

    ################ ! create so########################

    @api.depends()
    def _compute_now_stt(self):
        r = self.env['ir.model.data'].search(
            [('name', '=ilike', 'ndt_so%'), ('model', '=', 'sale.order')], limit=1, order='id desc')
        name = r.name
        if name:
            now_stt_rs = re.search('ndt_so.*(\d+)', name, re.I)
            self.now_stt = now_stt_rs.group(1)
        else:
            self.now_stt = 1

    ######### delete data ################

    @return_this_view_wrap
    def delete_xml_so_iv_do_data(self):
        r = self.env['ir.model.data'].search(
            [('module', '=', 'ndt_data_testf'), ('model', 'in', ['sale.order', 'sale.order.line'])])
        r.unlink()
        return self.return_this_view()

    @return_this_view_wrap
    def clean_master_data(self):
        raise UserError('Tạm thời không cho xóa')
        r = self.env['ir.model.data'].search(
            [('module', '=', 'ndt_data_testf')])
        r.unlink()

    @return_this_view_wrap
    def clean_master_data(self):
        print('unlink products')
        products = self.env['product.product'].search(
            [], order='id asc', offset=1)
        products.unlink()

        print('***unlink warehouse')

        first_wh = self.env['stock.warehouse'].search(
            [], order='id asc', limit=1)
        picking_types = self.env['stock.picking.type'].with_context(
            active_test=False).search([('warehouse_id', '!=', first_wh.id)])
        print('***picking_types')
        for picking_type in picking_types:
            print('***picking_type***', picking_type)
            # pr = self.env['procurement.rule'].with_context(active_test=False).search(['|','&', ('picking_type_id','=', picking_type.id),('active','=','True'),'&',('picking_type_id','=', picking_type.id), ('active','=','False')])

            pr = self.env['procurement.rule'].with_context(active_test=False).search(
                [('picking_type_id', '=', picking_type.id)])
            # pr = self.env['procurement.rule'].search([('picking_type_id','=', picking_type.id)])
            print('***pr*** xoa', pr)
            pr.unlink()

            # pr = self.env['procurement.rule'].search(['|', ('active','=','True'), ('active','=','False')])
            # print ('***pr 2*** xoa', pr)
            # pr.unlink()

        print('xoa picking_types')
        picking_types.unlink()

        print('unlink warehouse')
        wh = self.env['stock.warehouse'].search([], order='id asc', offset=1)
        wh.unlink()

        print('unlink company')
        cps = self.env['res.company'].search([], order='id asc', offset=1)
        cps.unlink()

        print('unlink users')
        users = self.env['res.users'].search([], order='id asc', offset=1)
        users.unlink()

    def clear_coa(self):
        CLD = self.env['ndt.clean.data']
        at = "account_tax"
        absl = "account_bank_statement_line"
        abs = "account_bank_statement"
        ppm = "pos_payment_method"
        aj = "account_journal"
        coa = "account_account"
        CLD.check_and_delete(at)
        CLD.check_and_delete(aj)
        CLD.check_and_delete(coa)

        return self.return_this_view()

    def clean_all_data(self):
        cl_obj = self.env['ndt.clean.data']
        cl_obj.clean_data(all_data=True, exclude=['cus_ven', 'tmpl'])
        self.rs = 'đã xóa sạch'
        return self.return_this_view()

    ######### ! delete data ################

    ######## râu ria ##############

    def increase_stt(self):
        if self.auto_increase_stt:
            self.stt = int(self.now_stt) + 1
        else:
            if self.now_stt:
                self.stt = self.now_stt
            else:
                self.stt = 1

    def return_this_view(self):
        return {
            'name': self._description,
            'view_mode': 'form',
            'view_id': self.env.ref('ndt_data_test.ndt_create_data_test_view').id,
            'res_model': self._name,
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'target': 'new'
        }

    @return_this_view_wrap
    def setting_common(self):
        rs = []
        rt = self.install_cao_for_all_company()
        rs.append(rt)

        rt = self.assign_cao_to_cate()
        rs.append(rt)

        self.rs = rs

    ################ !râu ria ####################

    ### Create master data############
    def create_master_data(self):
        rs = []
        print("##self.create_partner()")
        rt = self.create_partner()
        rs.append(rt)

        print("##Cài và gán định khoản")
        # tại sao bên kia thì chạy ok bên này bị lỗi

        print("##rt = self.create_company()")
        rt = self.create_company()
        rs.append(rt)

        self.setting_common()
        # print ("##self.create_company2()")
        # rt = self.create_company2()
        # rs.append(rt)

        print("##rt = self.on_group_multi_company_for_all_users()")
        # tại sao phải gán ở đây? chỉnh lên đa công ty thôi
        rt = self.on_group_multi_company_for_all_users()
        rs.append(rt)

        print("##self.create_user_admin1_belong_company1()")
        rt = self.create_user_admin1_belong_company1()
        rs.append(rt)

        print("##self.assign_admin_user_to_full_account()")
        rt = self.assign_admin_user_to_full_account()
        rs.append(rt)

        print("##self.create_product()")
        rt = self.create_product()
        rs.append(rt)
        pr = self.env['product.product'].browse(rt)
        pr.assign_cog_equal(standard_price=500)
        print("##self.create_promotion_product()")
        rt = self.create_promotion_product()
        rs.append(rt)

        self.rs = rs
        return self.return_this_view()

    ########base function #########

    def create_record_with_xmlid(self, name, model, vals):
        ir_model_data = self.env['ir.model.data']
        new_xml_id = name.replace(' ', '_')
        module = 'ndt_data_testf'
        rt = ir_model_data._update(model, module, vals, xml_id=new_xml_id,
                                   store=True, noupdate=False, mode='init', res_id=False)
        return rt

    ######## !base function #########

    ############ system master data###############
    # vì sao phải cài ndt_inochi_extend, vì install_vn_cao_for_a_company
    def install_module(self):
        to_install_modules = self.env['ir.module.module'].search(
            [('name', 'in', ['stock', 'sale', 'purchase', 'account_invoicing', 'ndt_account_reports_inherit', 'account_close_entry', 'ndt_inochi_extend'])])
        rs = to_install_modules.button_immediate_install()
        return rs

    def install_cao_for_all_company(self):
        rs = self.env["account.chart.template"].install_vn_cao_for_all_company()
        return {'install_cao_for_all_company': rs}

    #phải gán tự động định so_khoản cho cateogry
    def assign_cao_to_cate(self):
        cs = self.env['product.category'].search([])
        for c in cs:
            c.asign_account_account()
        return cs

    # unistall

    @return_this_view_wrap
    def uninstall_module(self):
        to_install_modules = self.env['ir.module.module'].search(
            [('name', 'in', ['stock'])])
        to_install_modules.button_immediate_uninstall()

    @return_this_view_wrap
    def uninstall_l10n_vn(self):
        m = self.env.ref('base.module_l10n_vn')
        m.button_immediate_uninstall()

    @return_this_view_wrap
    def install_l10n_vn(self):
        m = self.env.ref('base.module_l10n_vn')
        m.button_immediate_install()

    @return_this_view_wrap
    def upgrade_l10n_vn(self):
        m = self.env.ref('base.module_l10n_vn')
        m.button_immediate_upgrade()

    ############ !system master data###############
    ### product,partner,company master data #####
    ### !product,partner,company master data #####

    def assign_admin_user_to_full_account(self):
        ref = self.env.ref
        ag = self.env.ref('account.group_account_user')
        ur = ref('base.user_root')
        rs = ag.write(
            {'users': [(4, ur.id), (4, ref('ndt_data_testf.admin1').id)]})
        ur.write({
            'company_ids': [(4, ref('ndt_data_testf.company_1').id, 0), (4, ref('base.main_company').id, 0)]
        })
        return {'assign_admin_user_to_full_account': rs}

    def create_product(self):
        name = 'sp 1'
        model = 'product.product'
        vals = {
            'name': name,
            'standard_price': 500,
            'list_price': 1000,
            'type': 'product'
        }
        rt = self.create_record_with_xmlid(name, model, vals)
        return rt

    def asign_promotion_account_to_product(self, pr):
        for comp in self.env['res.company'].search([]):
            pr = pr.with_context(force_company=comp.id)
            pr.property_account_income_id = self.env['account.account'].search(
                [('code', '=', '5212'), ('company_id', '=', comp.id)])

    def create_promotion_product(self):
        name = 'gg 1'
        model = 'product.product'
        vals = {
            'name': name,
            'standard_price': 0,
            'list_price': -100,
            'type': 'service'
        }

        rt = self.create_record_with_xmlid(name, model, vals)
        pr = self.env[model].browse(rt)
        self.asign_promotion_account_to_product(pr)
        return rt

    def create_company(self):
        name = 'company 1'
        vals = {
            'name': name,
        }
        model = 'res.company'
        rt = self.create_record_with_xmlid(name, model, vals)
        return rt

    def create_company2(self):
        name = 'company 2'
        vals = {
            'name': name,
        }
        model = 'res.company'
        rt = self.create_record_with_xmlid(name, model, vals)
        return rt

    def create_partner(self):
        for so_kh in [1, 2]:
            name = 'kh %s' % so_kh
            vals = {
                'name': name,
                'supplier': 1
            }
            ir_model_data = self.env['ir.model.data']
            new_xml_id = name.replace(' ', '_')
            model = 'res.partner'
            module = 'ndt_data_testf'
            rt = ir_model_data._update(
                model, module, vals, xml_id=new_xml_id, store=True, noupdate=False, mode='init', res_id=False)
        return rt

    def create_user_admin1_belong_company1(self):
        name = 'admin1'
        ref = self.env.ref
        vals = {
            'login': name,
            'name': name,
            'password': 'admin',
            'groups_id': [(4, ref('base.group_system').id, 0)],
            'company_ids': [(4, ref('ndt_data_testf.company_1').id, 0), (4, ref('base.main_company').id, 0)]

        }
        model = 'res.users'
        rt = self.create_record_with_xmlid(name, model, vals)
        return rt

    def create_user_user1(self):
        name = 'user1'

        vals = {
            'name': name,
            'password': 'admin'
        }
        model = 'res.users'
        rt = self.create_record_with_xmlid(name, model, vals)
        return rt

    def on_group_multi_company_for_all_users(self):
        res_config_settings = self.env['res.config.settings']
        field = res_config_settings._fields.get('group_multi_company')

        Groups = self.env['res.groups']
        ref = self.env.ref

        field_group_xmlids = getattr(
            field, 'group', 'base.group_user').split(',')
        field_groups = Groups.concat(*(ref(it) for it in field_group_xmlids))

        implied_group = ref(field.implied_group)
        rs = field_groups.write({'implied_ids': [(4, implied_group.id)]})
        return rs


