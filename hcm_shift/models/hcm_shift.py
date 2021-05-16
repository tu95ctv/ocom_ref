# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from collections import defaultdict
from datetime import timedelta, datetime
import pytz
from odoo.exceptions import ValidationError

class ShiftHour(models.Model):
    _name = 'shift.hour'

    name = fields.Char()
    begin_hour = fields.Char(default='00:00')
    duration = fields.Float(default=7)
    company_id = fields.Many2one('res.company', string='Company', 
        required=True, default=lambda self: self.env.user.company_id)

class HCMShift(models.Model):
    _name = 'hcm.shift'
    _description = 'HCM Shift'

    image = fields.Binary()
    name = fields.Char(required=True)
    user_ids = fields.Many2many('res.users')
    task_ids = fields.One2many('shift.task','shift_id')
    date = fields.Date(default=lambda self: fields.Date.context_today(self), required=True)
    company_id = fields.Many2one('res.company', string='Company', 
        required=True, default=lambda self: self.env.user.company_id)
    shift_hour_id = fields.Many2one('shift.hour', required=True, default=1)
    begin_dt = fields.Datetime('Giờ bắt đầu', compute='_compute_begin_dt', store=True)
    end_dt = fields.Datetime('Giờ bắt đầu', compute='_compute_begin_dt', store=True)
    state = fields.Selection([('draft','draft'), ('confirm','confirm')])


    @api.depends('date','shift_hour_id')
    def _compute_begin_dt(self):
        for rec in self:

            input_date = rec.date
            begin_hour = rec.shift_hour_id.begin_hour
            duration = rec.shift_hour_id.duration

            dt = datetime.combine(input_date, datetime.strptime(begin_hour,'%H:%M').time())
            # utc_timezone = pytz.timezone('UTC')
            # hcm_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
            # dt = dt.replace(tzinfo=hcm_timezone).astimezone(utc_timezone).replace(tzinfo=None)
            dt = dt - timedelta(hours=7)
            rec.begin_dt = dt
            rec.end_dt = dt + timedelta(hours=duration)

    def button_1(self):
        rs = self.env['shift.task'].read_group([], ['parent_type'], ['parent_type'], lazy=False)
        res = []
        for i in rs:
            add_item = {}
            add_item['parent_type'] = i['parent_type']
            res.append(add_item)
            domain = i['__domain']
            rs2 = self.env['shift.task'].read_group(domain, ['company_id'], ['company_id'], lazy=False)
            for j in rs2:
                add_item2 = {}
                add_item2['company_id'] = j['company_id'] 
                res.append(add_item2)
                domain = i['__domain']
                rs3 = self.env['shift.task'].search(domain)
                add_item3 = {'ids':rs3}
                res.append(add_item3)
        print (res)

    def gen_line(self,name, level=1,colspan=1, columns = []):
        rs = {
            'name': name,
            # 'title_hover': '131 Trade receivables',
            'columns': columns,
            'level': level,
            # 'unfoldable': True,
            # 'unfolded': True,
            'colspan': colspan,
            # 'class': ''
        }
        return rs
   
    # def button_1(self):
    #     return self.xlsx_gen_line()

    def xlsx_gen_line(self):
        today = fields.Date.context_today(self)
        rs = self.env['shift.task'].search([('shift_id.date','=', today)])
        xlsx_rs = {}
        for sh in rs:
            type_group = xlsx_rs.setdefault(sh.parent_type,{})
            type_group['count'] = type_group.setdefault('count',0) + 1
            company_groups = type_group.setdefault('company_group',{})
            company_group = company_groups.setdefault(sh.company_id,{})
            company_group['count'] = company_group.setdefault('count',0) + 1
            ids = company_group.setdefault('ids',self.env['shift.task'])
            company_group['ids']  = company_group['ids'] + sh
        lines = []
        for parent_type, v in xlsx_rs.items():
            # parent_type_line = [parent_type, v['count']]
            parent_type_line = self.gen_line(parent_type, columns=[{'name': v['count']}], level=1)
            lines.append(parent_type_line)
            company_group = v['company_group']
            for company, v in company_group.items():
                # company_line = [{'company':company}, {'count':v['count']}]
                company_line = self.gen_line(company.name, columns=[{'name': v['count']}], level=2)
                lines.append(company_line)
                ids = v['ids']
                for sh in ids:
                    sh_line = self.gen_line('',colspan = 4, columns=[{'name': sh.name}], level=3)
                    lines.append(sh_line)
        print (xlsx_rs)
        print (lines)
        return lines

    @api.constrains('begin_dt')
    def date_begin_constrains(self):
        for r in self:
            for task in r.task_ids:
                task.validation_date_begin()

class TaskType(models.Model):
    _name = 'shift.task.type'
    _description = 'Shift Task'

    name = fields.Char()
    parent_type = fields.Selection([('trouble','Sự cố'), ('task','Công việc')])


class Task(models.Model):
    _name = 'shift.task'
    _description = 'Shift Task'

    name = fields.Char(required=True)
    shift_id = fields.Many2one('hcm.shift')
    date_begin = fields.Datetime(string='Begin Date', default=fields.Datetime.now, required=True)
    date_end = fields.Datetime(string='Ending Date')
    type_id = fields.Many2one('shift.task.type', ondelete='restrict')
    partner_ids = fields.Many2many('res.partner')
    parent_type = fields.Selection([('trouble','Sự cố'), ('task','Công việc')])
    company_id = fields.Many2one('res.company', string='Company', 
        required=True, default=lambda self: self.env.user.company_id)

    def validation_date_begin(self):
        r = self
        if r.date_begin:
            diff = r.date_begin - r.shift_id.end_dt
            diff_in_s = diff.total_seconds()
            diff_in_hour = diff_in_s/3600.0
            print ('***diff_in_hour', diff_in_hour)
            if diff_in_hour > 2:
                raise ValidationError('Giờ bắt đầu của task không được lớn hơn giờ kết ca quá 2 tiếng')

            diff = r.shift_id.begin_dt - r.date_begin
            diff_in_s = diff.total_seconds()
            diff_in_hour = diff_in_s/3600.0
            if diff_in_hour > 1:
                raise ValidationError('Giờ bắt đầu của task không được sớm hơn giờ bắt đầu ca quá 1 tiếng')
   
    @api.constrains('date_begin')
    def date_begin_constrains(self):
        print ('aaaaaaaaaaaaaaaaaaaaaaaaaa')
        for r in self:
            r.validation_date_begin
            


            

            