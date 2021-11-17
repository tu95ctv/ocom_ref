# -*- coding: utf-8 -*-
import re
import base64
from odoo import models, fields, api
from odoo.exceptions import UserError
from unidecode import unidecode
import datetime
from odoo.addons.bds.models.bds_tools  import  request_html
from odoo.exceptions import UserError
from odoo.addons.bds.models.bds_tools import g_or_c_ss
from odoo.addons.bds.models.main_fetch_common  import  _compute_so_phong_ngu,\
    _compute_dd_tin_cua_dau_tu, _compute_loai_hem_combine, _compute_kw_mg
from odoo.addons.bds.models.compute_choosed_area  import _compute_choosed_area_muc_gia
import psycopg2
import operator
from odoo.addons.bds.models.bds_tools import convert_text_to_json

def skip_if_cate_not_bds(depend_func):
    def wrapper(*args,**kargs):
        self = args[0]
        for r in self:
            if r.cate ==u'bds':
                depend_func(r)
    return wrapper

class UserReadMark(models.Model):
    _name = 'user.read.mark'

    user_id = fields.Many2one('res.users')
    bds_id = fields.Many2one('bds.bds')

class UserQuanTamMark(models.Model):
    _name = 'user.quantam.mark'

    user_id = fields.Many2one('res.users')
    bds_id = fields.Many2one('bds.bds')

# def _compute_slug(name, id):
#     name = unidecode(name)
#     name = re.sub('\s+','-',name)
#     name = re.sub('\W','-',name, flags=re.I)
#     name = re.sub('-{2,}','-', name)
#     name = name.lower()
#     name  = name + '_' + str(id)
#     return name

class BDSCate(models.Model):
    _name = 'bds.cate'

    name = fields.Char()
    parent_id = fields.Many2one('bds.cate')
    description = fields.Char()

class bds(models.Model):
    _name = 'bds.bds'
    _order = "id desc"
    _rec_name = 'title'

    sql_constraints = [
        ('slug_uniq', 'unique(slug)', "A slug can only be assigned to one bds !"),
    ]
    slug = fields.Char()
    cate_id = fields.Many2one('bds.cate')        
    trigger = fields.Boolean()
    state_district_ward_nok = fields.Char()
    so_lan_diff_public_update = fields.Integer()
    so_lan_gia_update = fields.Integer()
    vip = fields.Char()
    user_read_mark_ids = fields.One2many('user.read.mark','bds_id')
    user_quantam_mark_ids = fields.One2many('user.quantam.mark','bds_id')
    sell_or_rent =  fields.Selection([('sell','sell'), ('rent', 'rent'),
        ('need_to_buy','need_to_buy')], default='sell')
    loai_nha = fields.Char('Loại nhà')
    loai_nha_selection = fields.Selection([('Căn hộ/Chung cư','Căn hộ/Chung cư'),
                                 ('Nhà ở','Nhà ở'),
                                 ('Đất', 'Đất'),
                                 ('Văn phòng, Mặt bằng kinh doanh','Văn phòng, Mặt bằng kinh doanh'),
                                 ('Phòng trọ', 'Phòng trọ'),# loai_nha của chợ tốt
                               ], string='Loại nhà')
    link = fields.Char()
    cate = fields.Char(default='bds')
    url_id = fields.Many2one('bds.url')
    title = fields.Char(required=True)
    images_ids = fields.One2many('bds.images', 'bds_id' )
    siteleech_id = fields.Many2one('bds.siteleech')
    thumb = fields.Char()
    poster_id = fields.Many2one('bds.poster')#, ondelete='restrict'
    html = fields.Html()
    chotot_moi_gioi_hay_chinh_chu = fields.Selection([('moi_gioi', 'Bán chuyên'), 
        ('chinh_chu', 'Cá nhân'),('khong_biet','Không Phải bài ở chợt tốt')], default='khong_biet',string='Bán chuyên')
    gia = fields.Float('Giá')
    gia_trieu = fields.Float()
    price = fields.Float()
    price_unit = fields.Char()
    area = fields.Float(digits=(32,1),string='Diện tích')
    address=fields.Char()
    district_id = fields.Many2one('res.country.district', string='Quận')
    state_id = fields.Many2one('res.country.state',related='district_id.state_id', store=True)
    ward_id = fields.Many2one('res.country.ward','Phường')
    date_text = fields.Char()
    public_datetime = fields.Datetime()
    diff_public_datetime = fields.Integer()
    public_date = fields.Date()
    diff_public_date = fields.Integer()
    publicdate_ids =fields.One2many('bds.publicdate','bds_id')
    gialines_ids = fields.One2many('bds.gialines','bds_id')
    diff_gia = fields.Float()
    ngay_update_gia = fields.Datetime()
    #set field (field mà mình điền vào)
    is_read = fields.Boolean()
    quan_tam = fields.Datetime(string=u'Quan Tâm')
    ko_quan_tam = fields.Datetime(string=u'Không Quan Tâm')
    nganh_nghe_kinh_doanh = fields.Char()
    name_of_poster = fields.Char()
    # related no store
    muc_gia_quan = fields.Float(related='district_id.muc_gia_quan')
    post_ids_of_user  = fields.One2many('bds.bds','poster_id', related='poster_id.post_ids')
    #related store
    detail_du_doan_cc_or_mg = fields.Selection(related='poster_id.detail_du_doan_cc_or_mg', store = True)
    du_doan_cc_or_mg = fields.Selection(related='poster_id.du_doan_cc_or_mg', store = True)
    count_post_all_site = fields.Integer(related= 'poster_id.count_post_all_site',store=True)

    
    dd_tin_cua_co_rate = fields.Float(related='poster_id.dd_tin_cua_co_rate')
    dd_tin_cua_dau_tu_rate = fields.Float(related='poster_id.dd_tin_cua_dau_tu_rate')
    #!related store

    # for filter field
    district_id_selection = fields.Selection('get_quan_')
    siteleech_id_selection = fields.Selection('siteleech_id_selection_')
    greater_day = fields.Integer()# for search field
    # !for filter field



    # compute no store
    html_show = fields.Html(compute='html_show_',string=u'Nội dung')
    html_show_laptop = fields.Html(compute='html_show_laptop_',string=u'Nội dung')
    html_replace = fields.Html(compute='html_replace_')
    link_show =  fields.Char(compute='link_show_')
    cho_tot_link_fake = fields.Char(compute='cho_tot_link_fake_')
    thumb_view = fields.Binary(compute='thumb_view_')  
    is_user_read_mark = fields.Boolean(compute='_is_user_read_mark')
    is_user_quantam_mark = fields.Boolean(compute='_is_user_quantam_mark')
    diff_public_days_from_now = fields.Integer(compute='_compute_diff_public_days_from_now')
    #! compute no store

    #compute field#store field
    html_khong_dau = fields.Html()
    so_phong_ngu = fields.Integer()
 
    
    same_address_bds_ids = fields.Many2many('bds.bds','same_bds_and_bds_rel','same_bds_id','bds_id')
    trich_dia_chi = fields.Char( string='Trích địa chỉ')
    mat_tien_address = fields.Char()
    mat_tien_or_trich_dia_chi = fields.Char()
    is_mat_tien_or_trich_dia_chi = fields.Selection([('1','Có trích địa chỉ hoặc mặt tiền'),
        ('0','Không Có trích địa chỉ hoặc mặt tiền' )])


    

    dd_tin_cua_co = fields.Selection([('kw_co_cap_1', 'Keyword cò cấp 1'),
        ('no_kw_co_cap_1', 'Không f cò cấp 1')], string='is có kw môi giới')
    kw_mg = fields.Char(string='kw môi giới')
    kw_mg_cap_2= fields.Char(string='kw môi giới cấp 2')
    is_kw_mg_cap_2= fields.Char(string='kw môi giới cấp 2')
    kw_co_date = fields.Char()
    kw_co_break = fields.Integer()
    kw_co_special_break = fields.Integer()
    kw_co_mtg = fields.Char()
    number_char = fields.Integer()
    hoa_la_canh = fields.Char()
    t1l1 = fields.Char()


    dd_tin_cua_dau_tu = fields.Boolean(string='kw đầu tư')
    kw_hoa_hong = fields.Char(store=True)
    kw_so_tien_hoa_hong = fields.Char(store=True)

    hem_rong = fields.Float()
    hem_rong_char = fields.Char()
    loai_hem_selection = fields.Selection([('hxh','hxh'), ('hxt','hxt'), ('hxm','hxm'), ('hbg','hbg')])
    loai_hem_combine = fields.Selection([('mt','mặt tiền'), ('hxh','hxh'), ('hxt','hxt'), ('hbg','hbg'), ('hxm','hxm')])
    mat_tien = fields.Char()
    full_mat_tien = fields.Char()
    is_mat_tien = fields.Boolean()

    muc_gia = fields.Selection([('0','0'), ('<1','<1'),('1-2','1-2'),('2-3','2-3'),
                                ('3-4','3-4'),('4-5','4-5'),('5-6','5-6'),
                                ('6-7','6-7'),('7-8','7-8'),('8-9','8-9'),
                                ('9-10','9-10'),('10-11','10-11'),('11-12','11-12'),('>12','>12')], string=u'Mức Giá')
    muc_dt = fields.Selection(
        [('0','0'), ('<10','<10'),('10-20','10-20'),('20-30','20-30'),('30-40','30-40'),
        ('40-50','40-50'),('50-60','50-60'),('60-70','60-70'),('>70','>70')],string=u'Mức diện tích')
    muc_don_gia = fields.Selection([('0','0'),('0-30','0-30'),('30-60','30-60'),('60-90','60-90'),
                                    ('90-120','90-120'),('120-150','120-150'),('150-180','150-180'),
                                    ('180-210','180-210'),('>210','>210')])
    ti_le_don_gia = fields.Float(digits=(6,2))
    muc_ti_le_don_gia = fields.Selection([('0','0'), ('0-0.4','0-0.4'),('0.4-0.8','0.4-0.8'),('0.8-1.2','0.8-1.2'),
                                    ('1.2-1.6','1.2-1.6'),('1.6-2.0','1.6-2.0'),('2.0-2.4','2.0-2.4'),
                                    ('2.4-2.8','2.4-2.8'),('>2.8','>2.8')])
    auto_ngang = fields.Float()
    auto_doc = fields.Float()
    auto_dien_tich = fields.Float(digits=(6,2))
    ti_le_dien_tich_web_vs_auto_dien_tich = fields.Float(digits=(6,2))
    don_gia = fields.Float(digit=(6,2),string=u'Đơn giá')
    choose_area = fields.Float(digits=(6,2))#,store=True
    so_lau = fields.Float(digits=(6,1))
    so_lau_he_so = fields.Float(digits=(6,1))
    so_lau_char = fields.Char()
    dtsd = fields.Float(digits=(6,2))
    dtsd_tu_so_lau = fields.Float(digits=(6,2))
    ti_le_dtsd = fields.Float(digits=(6,2))
    dtsd_combine = fields.Float(digits=(6,2))
    gia_xac_nha = fields.Float(digits=(6,2))
    gia_dat_con_lai = fields.Float(digits=(6,2))
    don_gia_dat_con_lai = fields.Float(digits=(6,2))
    ti_le_don_gia_dat_con_lai = fields.Float(digits=(6,2))
    don_gia_quan = fields.Float(digits=(6,2))
    
    # function not depends
    def search(self, args, **kwargs):
        try:
            rs = args.index(1)
        except:
            rs = None
        if rs !=None:
            rs = args.index(1)
            del args[rs]
            user_read_mark = self.env['user.read.mark'].search([('user_id','=',self.env.uid)])
            user_read_mark_bds_ids = user_read_mark.mapped('bds_id')
            if user_read_mark_bds_ids:
                args += [['id', 'not in', user_read_mark_bds_ids]]
        return super(bds, self).search(args, **kwargs)

    # function not depends
    def search(self, args, **kwargs):
        if not args:
            args = []
        if self._context.get('search_user_not_read'):
            user_read_mark = self.env['user.read.mark'].search([('user_id','=',self.env.uid)])
            user_read_mark_bds_ids = user_read_mark.mapped('bds_id.id')
            if user_read_mark_bds_ids:
                args += [['id', 'not in', user_read_mark_bds_ids]]
          
        return super(bds, self).search(args, **kwargs)

    @api.model
    def create(self, vals):
        r = super(bds,self).create(vals)
        try:
            pass
            r.count_post_of_poster_() # bỏ đi để coi hết cảnh báo trên version 13 không
        except psycopg2.extensions.TransactionRollbackError:
            pass
        return r

    def make_trigger(self):
        for r in self:
            r.trigger = True

    # method out function
   
    def user_read_mark(self):
        for r in self:
            user = self.env.user
            bds_id = r
            user_read_mark = self.env['user.read.mark'].search([('user_id','=',user.id), ('bds_id','=',bds_id.id)])
            if not user_read_mark:
                self.env['user.read.mark'].create({'user_id':user.id, 'bds_id':bds_id.id })
    
    def user_not_read_mark(self):
        for r in self:
            user = self.env.user
            bds_id = r
            user_read_mark = self.env['user.read.mark'].search([('user_id','=',user.id), ('bds_id','=',bds_id.id)])
            user_read_mark.unlink()

    def user_quantam_mark(self):
        for r in self:
            user = self.env.user
            bds_id = r
            user_read_mark = self.env['user.quantam.mark'].search([('user_id','=',user.id), ('bds_id','=',bds_id.id)])
            if not user_read_mark:
                self.env['user.quantam.mark'].create({'user_id':user.id, 'bds_id':bds_id.id })
    
    def user_not_quantam_mark(self):
        for r in self:
            user = self.env.user
            bds_id = r
            user_read_mark = self.env['user.quantam.mark'].search([('user_id','=',user.id), ('bds_id','=',bds_id.id)])
            user_read_mark.unlink()

    def open_something(self):
        return {
                'name': 'abc',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'bds.bds',
                # 'view_id': self.env.ref('bds.bds_form').id,
                'type': 'ir.actions.act_window',
                'res_id': self.id,
                'target': 'new'
            }

    def set_quan_tam(self):
        for r in self:
            r.quan_tam = fields.Datetime.now()

    def siteleech_id_selection_(self):
        rs = list(map(lambda i:(i.name,i.name),self.env['bds.siteleech'].search([])))
        return rs

    def get_quan_(self):
        quans = self.env['res.country.district'].search([])
        rs = list(map(lambda i:(i.name,i.name),quans))
        return rs

    # no store
    def _is_user_quantam_mark(self):
        for r in self:
            user = self.env.user
            bds_id = r
            is_user_quantam_mark = self.env['user.quantam.mark'].search([('user_id','=',user.id), ('bds_id','=',bds_id.id)])
            r.is_user_quantam_mark = bool(is_user_quantam_mark)

    def _is_user_read_mark(self):
        for r in self:
            user = self.env.user
            bds_id = r
            user_read_mark = self.env['user.read.mark'].search([('user_id','=',user.id), ('bds_id','=',bds_id.id)])
            r.is_user_read_mark = bool(user_read_mark)

    @api.depends('public_date')
    def _compute_diff_public_days_from_now(self):
        for r in self:
            if r.public_date:
                print ('kakaka', type( r.public_date))
                r.diff_public_days_from_now = (fields.Date.today() - r.public_date).days
            else:
                r.diff_public_days_from_now = False

    @api.depends('html')
    @skip_if_cate_not_bds
    def html_replace_(self):
        for r in self:
            html =  r.html
            html_replace = re.sub('[\d. ]{10,11}','',html)# replace số điện thoại
            if r.trich_dia_chi:
                html_replace = html_replace.replace(r.trich_dia_chi,'')
            r.html_replace = html_replace

    @api.depends('html')
    def html_show_(self):
        khong_hien_thi_nhieu_html = self.env['ir.config_parameter'].sudo().get_param('bds.khong_hien_thi_nhieu_html')
        for r in self:
            r.html_show = 'id:%s <b>%s</b>'%(r.id, r.title if r.title else '') + \
            ('\n' + '<b>%s</b>'%r.district_id.name if r.district_id.name  else '') +\
            ('\n<br>' + r.html if r.html else '') +\
            ('\n<br>Phone: ' + (r.poster_id.name or '')) +\
            ('\n<br>detail_du_doan_cc_or_mg: %s'%r.poster_id.detail_du_doan_cc_or_mg) +\
            (
            (
            ('\n<br>' +r.link_show if  r.link_show else '')+ \
            ('\n<br> Giá: <b>%s tỷ</b>'%(r.gia if r.gia else '')) +\
            ('\n<br> kích thước: %s'%('<b>%sm x %sm</b>'%(r.auto_ngang, r.auto_doc) if (r.auto_ngang or r.auto_doc) else ''))+\
            ('\n<br> Area: %s'%('<b>%s m2</b>'%r.area if r.area else ''))+\
            ('\n<br> auto_dien_tich: %s'%('<b>%s m2</b>'%r.auto_dien_tich if r.auto_dien_tich else ''))+\
            ('\n<br> Chọn lại diện tích: %s'%('<b>%s m2</b>'%r.choose_area if r.choose_area else ''))+\
            ('\n<br>địa chỉ: %s'%(r.trich_dia_chi or r.mat_tien_address)) +\
            ('\n<br>Site: %s'%r.siteleech_id.name) +\
            ('\n<br>Đơn giá: %.2f'%r.don_gia) + \
            ('\n<br>Tỉ lệ đơn giá: %.2f'%r.ti_le_don_gia)  + \
            ('\n<br>Tổng số bài của người này: <b>%s</b>'%r.count_post_all_site) +\
            ('\n<br>Chợ tốt CC or MG: %s' %dict(self.env['bds.bds']._fields['chotot_moi_gioi_hay_chinh_chu'].selection).get(r.chotot_moi_gioi_hay_chinh_chu))+\
            ('\n<br>du_doan_cc_or_mg: <b>%s </b>'%dict(self.env['bds.poster']._fields['du_doan_cc_or_mg'].selection).get(r.poster_id.du_doan_cc_or_mg))+\
            ('\n<br> address_rate: %s'%r.poster_id.address_rate) +\
            ('\n<br>tỉ lệ keyword cò : %s'%r.poster_id.dd_tin_cua_co_rate) +\
            ('\n<br>tỉ lệ keyword đầu tư: %s'%r.poster_id.dd_tin_cua_dau_tu_rate) +\
            ('\n<br>public_date %s'%r.public_date)
            ) if not khong_hien_thi_nhieu_html else '')

    @api.depends('html')
    def html_show_laptop_(self):
        for r in self:
            r.html_show_laptop = 'id:%s <b>%s</b>'%(r.id, r.title if r.title else '') + \
            ('\n<br>' + r.html if r.html else '') 
            
                    
    def link_show_(self):
        for r in self:
            if r.siteleech_id.name == 'chotot':
                r.link_show = r.cho_tot_link_fake
            else:
                r.link_show = r.link
                
    @api.depends('link')
    def cho_tot_link_fake_(self):
        for r in self:
            if r.link and 'chotot' in r.link:
                rs = re.search('/(\d*)$',r.link)
                id_link = rs.group(1)
                r.cho_tot_link_fake = 'https://nha.chotot.com/nhadat/mua-ban-nha-dat/'  + id_link+ '.htm'
                
    @api.depends('thumb')
    def thumb_view_(self):
        for r in self:
            
            if r.thumb:
                if 'nophoto' not in r.thumb:
                    photo = base64.encodestring(request_html(r.thumb, False, is_decode_utf8 = False))
                    r.thumb_view = photo 
            else:
                r.thumb_view = False

    # out function 
    def send_mail_chinh_chu(self):
        body_html = ''
        minutes = int(self.env['ir.config_parameter'].sudo().get_param('bds.interval_mail_chinh_chu_minutes',default=0))
        if minutes ==0:
            minutes=5
        gia = float(self.env['ir.config_parameter'].sudo().get_param('bds.gia',default=0))
        if gia ==0:
            gia =13
        minutes_5_last = fields.Datetime.now() -   datetime.timedelta(minutes=minutes, seconds=1)
        cr = self.search([('create_date','>', minutes_5_last),
            ('district_id.name', 'in',['Quận 1','Quận 3', 'Quận 5', 'Quận 10', 'Quận Tân Bình', 'Quận Tân Phú', 'Quận Phú Nhuận', 'Quận Bình Thạnh']),
            '|', '&', ('trich_dia_chi','!=',False), ('gia','<', gia), '&', ('mat_tien_address','!=',False), ('gia','<', 13)
            ])
        if cr:
            for r in cr:
                one_mail_html = r.html_show
                images = r.images_ids
                image_tags = map(lambda i: '<img src="%s" style="width:300px" alt="Girl in a jacket">'%i, list(images.mapped('url')) + [r.thumb])
                image_html = '<br>'.join(image_tags)
                one_mail_html += '<br>' + image_html

                body_html += '<br><br><br>' + one_mail_html
            email_to = self.env['ir.config_parameter'].sudo().get_param('bds.email_to')
            if email_to:
                email_to = email_to.split(',')
            else:
                email_to = []
            email_to.append('nguyenductu@gmail.com')
            email_to = ','.join(email_to)
            mail_id = self.env['mail.mail'].create({
                'subject':'%s topic chính chủ trong 5 phút qua'%(len(cr)),
                'email_to':email_to,
                'body_html': body_html,
                })
            mail_id.send()

    def cronjob_trich_dia_chi_tieu_chi(self):
        query = 'select count(mat_tien_address) as count,mat_tien_address,poster_id,siteleech_id from bds_bds where mat_tien_address is not null group by mat_tien_address,poster_id,siteleech_id having count(mat_tien_address) > 2 ORDER BY count desc limit 3'
        query = 'select count(trich_dia_chi) as count,trich_dia_chi,poster_id,siteleech_id from bds_bds where trich_dia_chi is not null group by trich_dia_chi,poster_id,siteleech_id having count(trich_dia_chi) > 0 ORDER BY count desc limit 3'
        self.env.cr.execute(query)
        rss = self.env.cr.fetchall()
        for rs in rss:
            search_dict = {'tieu_chi_char_1':rs[1], 'tieu_chi_int_2':rs[3], 'tieu_chi_int_2':rs[2]} # tieu_chi_int_2: siteleech_id
            update_dict = {'tieu_chi_int_1':rs[0]}#tieu_chi_int_1: count
            quan = g_or_c_ss(self.env['bds.tieuchi'],search_dict, update_dict )
        

    def test(self):
        readgroup_rs = self.env['bds.bds'].read_group([('don_gia','>=', 20), ('don_gia','<=', 300),('poster_id','=',18)],['district_id','siteleech_id','avg_gia:avg(gia)','count(district_id)'],['district_id','siteleech_id'], lazy=False)
        raise UserError(str(readgroup_rs))

    def test2(self):
        rs = self.env['ir.config_parameter'].get_param("bds.loai_nha")
        rs = eval(rs)
        raise UserError('%s-%s'%(type(rs),str(rs)))

    ##### thống kê cò hay đầu tư 
    def du_doan_cc_or_mg_(self,address_rate, chotot_mg_or_cc, dd_tin_cua_co_count,
        count_post_of_onesite_max, dd_tin_cua_dau_tu_count):
        if chotot_mg_or_cc =='moi_gioi' :
            if address_rate > 0.5:
                du_doan_cc_or_mg= 'dd_cc'
                detail_du_doan_cc_or_mg = 'dd_cc_b_moi_gioi_n_address_rate_gt_0_5'
            else:
                du_doan_cc_or_mg= 'dd_mg'
                detail_du_doan_cc_or_mg = 'dd_mg_b_moi_gioi_n_address_rate_lte_0_5'
        elif dd_tin_cua_co_count:
            if address_rate > 0.5:
                du_doan_cc_or_mg= 'dd_cc'
                detail_du_doan_cc_or_mg = 'dd_cc_b_kw_co_n_address_rate_gt_0_5'
            else:
                du_doan_cc_or_mg= 'dd_mg'
                detail_du_doan_cc_or_mg = 'dd_mg_b_kw_co_n_address_rate_lte_0_5'
        else:
            if chotot_mg_or_cc =='chinh_chu':
                if count_post_of_onesite_max > 3:
                    if address_rate > 0:
                        du_doan_cc_or_mg= 'dd_cc'
                        detail_du_doan_cc_or_mg = 'dd_cc_b_chinh_chu_n_cpas_gt_3_n_address_rate_gt_0'
                    else:
                        du_doan_cc_or_mg= 'dd_mg'
                        detail_du_doan_cc_or_mg = 'dd_mg_b_chinh_chu_n_cpas_gt_3_n_address_rate_eq_0'
                else:
                    du_doan_cc_or_mg= 'dd_cc'
                    if address_rate > 0:
                        detail_du_doan_cc_or_mg = 'dd_cc_b_chinh_chu_n_cpas_lte_3_n_address_rate_gt_0_sure'
                    else:
                        detail_du_doan_cc_or_mg = 'dd_cc_b_chinh_chu_n_cpas_lte_3_n_address_rate_eq_0_nosure' 
            else:#khong_biet, muaban
                if count_post_of_onesite_max  > 3:
                    if address_rate >= 0.3:
                        du_doan_cc_or_mg= 'dd_cc'
                        detail_du_doan_cc_or_mg = 'dd_cc_b_khong_biet_n_cpas_gt_3_n_address_rate_gte_0_3'
                    else:
                        du_doan_cc_or_mg= 'dd_mg'
                        detail_du_doan_cc_or_mg = 'dd_mg_b_khong_biet_n_cpas_gt_3_n_address_rate_lt_0_3'
                        
                else: #count_post_of_onesite_max  <= 3
                    if address_rate: 
                        du_doan_cc_or_mg= 'dd_cc'
                        detail_du_doan_cc_or_mg = 'dd_cc_b_khong_biet_n_cpas_lte_3_n_address_rate_gt_0'
                    else:
                        du_doan_cc_or_mg= 'dd_kb'
                        detail_du_doan_cc_or_mg = 'dd_kb_b_khong_biet_n_cpas_lte_3_n_address_rate_eq_0'

        if du_doan_cc_or_mg !='dd_mg':
            if  dd_tin_cua_dau_tu_count:
                du_doan_cc_or_mg= 'dd_dt'
        return du_doan_cc_or_mg, detail_du_doan_cc_or_mg


    def site_post_count_(self,site_post_count,  bds_id__siteleech_id__id):
        one_site_post_count = site_post_count.get(str(bds_id__siteleech_id__id),0)
        site_post_count[str(bds_id__siteleech_id__id)] = one_site_post_count + 1
        site_and_count_max = max(site_post_count.items(), key=operator.itemgetter(1))
        count_post_of_onesite_max = site_and_count_max[1]
        siteleech_max_id = int(site_and_count_max[0])
        len_site = len(site_post_count)
        return count_post_of_onesite_max,siteleech_max_id, len_site, site_post_count


    def du_doan_tin_cua_co_(self, bds_id__dd_tin_cua_co, dd_tin_cua_co_count,
        bds_id__dd_tin_cua_dau_tu, dd_tin_cua_dau_tu_count, count_post_all_site):
        dd_tin_cua_co_rate = False
        dd_tin_cua_dau_tu_rate = False
        if bds_id__dd_tin_cua_co == 'kw_co_cap_1':
            dd_tin_cua_co_count +=1
            dd_tin_cua_co_rate = dd_tin_cua_co_count/count_post_all_site
        if bds_id__dd_tin_cua_dau_tu:
            dd_tin_cua_dau_tu_count +=1
            dd_tin_cua_dau_tu_rate = dd_tin_cua_dau_tu_count/count_post_all_site
        return dd_tin_cua_co_count, dd_tin_cua_dau_tu_count, dd_tin_cua_co_rate, dd_tin_cua_dau_tu_rate
    
    def cho_tot_cc_(self, bds_id__siteleech_id__name,bds_id__chotot_moi_gioi_hay_chinh_chu, chotot_count, chotot_mo_gioi_count, chotot_chinh_chu_count):
        if bds_id__siteleech_id__name =='chotot':
            chotot_count +=1
            if bds_id__chotot_moi_gioi_hay_chinh_chu =='moi_gioi':
                chotot_mo_gioi_count += 1
            else:
                chotot_chinh_chu_count += 1
        if chotot_mo_gioi_count:
            chotot_mg_or_cc = 'moi_gioi'
        else:
            if chotot_chinh_chu_count:
                chotot_mg_or_cc = 'chinh_chu'
            else:
                chotot_mg_or_cc = 'khong_biet'
        return chotot_mo_gioi_count, chotot_chinh_chu_count, chotot_mg_or_cc

    
    def _thong_ke_co_hay_cc(self, bds_id__siteleech_id__id,bds_id__mat_tien_or_trich_dia_chi, site_post_count,count_post_all_site,
        address_topic_number, guess_count, dd_tin_cua_co_count, bds_id__dd_tin_cua_co, dd_tin_cua_dau_tu_count,
        bds_id__dd_tin_cua_dau_tu,chotot_count, chotot_mo_gioi_count, chotot_chinh_chu_count, bds_id__siteleech_id__name,
        bds_id__chotot_moi_gioi_hay_chinh_chu):
        
        poster_dict = {}
        if not bds_id__siteleech_id__id:
            return poster_dict

        count_post_of_onesite_max,siteleech_max_id, len_site, site_post_count = \
            self.site_post_count_(site_post_count,  bds_id__siteleech_id__id)
        poster_dict['len_site'] = len_site
        poster_dict['site_post_count'] = site_post_count
        poster_dict['count_post_of_onesite_max'] = count_post_of_onesite_max
        poster_dict['siteleech_max_id'] = siteleech_max_id

        count_post_all_site = count_post_all_site + 1
        poster_dict['count_post_all_site'] = count_post_all_site
        
        address_rate = False
        if bds_id__mat_tien_or_trich_dia_chi:
            address_topic_number = address_topic_number + 1
        address_rate = address_topic_number/count_post_all_site
        
        poster_dict['address_topic_number'] = address_topic_number
        if address_rate:
            poster_dict['address_rate'] = address_rate
            guess_count['address_rate'] = address_rate
        poster_dict['guess_count'] = guess_count
        
        dd_tin_cua_co_count, dd_tin_cua_dau_tu_count, dd_tin_cua_co_rate, dd_tin_cua_dau_tu_rate = \
            self.du_doan_tin_cua_co_(bds_id__dd_tin_cua_co, dd_tin_cua_co_count,
            bds_id__dd_tin_cua_dau_tu, dd_tin_cua_dau_tu_count, count_post_all_site)

        guess_count['dd_tin_cua_co_count'] = dd_tin_cua_co_count
        if dd_tin_cua_co_rate:
            poster_dict['dd_tin_cua_co_rate'] = dd_tin_cua_co_rate
        poster_dict['dd_tin_cua_co_count'] = dd_tin_cua_co_count
        
        guess_count['dd_tin_cua_dau_tu_count'] = dd_tin_cua_dau_tu_count
        if dd_tin_cua_dau_tu_rate:
            poster_dict['dd_tin_cua_dau_tu_rate'] = dd_tin_cua_dau_tu_rate
        poster_dict['dd_tin_cua_dau_tu_count'] = dd_tin_cua_dau_tu_count

        chotot_mo_gioi_count, chotot_chinh_chu_count, chotot_mg_or_cc = \
            self.cho_tot_cc_(bds_id__siteleech_id__name,bds_id__chotot_moi_gioi_hay_chinh_chu,
                chotot_count, chotot_mo_gioi_count, chotot_chinh_chu_count)
        
        if bds_id__siteleech_id__name =='chotot':
            poster_dict['chotot_count'] = chotot_count
            guess_count['chotot_mo_gioi_count'] = chotot_mo_gioi_count
            poster_dict['chotot_mo_gioi_count'] = chotot_mo_gioi_count
            guess_count['chotot_chinh_chu_count'] = chotot_chinh_chu_count
            poster_dict['chotot_chinh_chu_count'] = chotot_chinh_chu_count


        poster_dict['chotot_mg_or_cc'] = chotot_mg_or_cc
        guess_count['chotot_mg_or_cc'] = chotot_mg_or_cc
        
        du_doan_cc_or_mg,detail_du_doan_cc_or_mg =  self.du_doan_cc_or_mg_(address_rate, chotot_mg_or_cc, dd_tin_cua_co_count,
        count_post_of_onesite_max, dd_tin_cua_dau_tu_count)
        poster_dict['du_doan_cc_or_mg'] = du_doan_cc_or_mg
        poster_dict['detail_du_doan_cc_or_mg'] = detail_du_doan_cc_or_mg
        return poster_dict

    # gọi hàm này sau khi lưu bds
    def count_post_of_poster_(self):
        bds_id =self 
        poster = bds_id.poster_id    
        
        bds_id__siteleech_id__id = bds_id.siteleech_id.id
        bds_id__mat_tien_or_trich_dia_chi = bds_id.mat_tien_or_trich_dia_chi
        bds_id__dd_tin_cua_co = bds_id.dd_tin_cua_co
        bds_id__siteleech_id__name = bds_id.siteleech_id.name
        bds_id__chotot_moi_gioi_hay_chinh_chu = bds_id.chotot_moi_gioi_hay_chinh_chu
        bds_id__dd_tin_cua_dau_tu = bds_id.dd_tin_cua_dau_tu

        site_post_count = poster.site_post_count
        site_post_count = convert_text_to_json(site_post_count)
        count_post_all_site = poster.count_post_all_site
        address_topic_number = poster.address_topic_number
        guess_count  = convert_text_to_json(poster.guess_count)
        dd_tin_cua_co_count = poster.dd_tin_cua_co_count
        dd_tin_cua_dau_tu_count  = poster.dd_tin_cua_dau_tu_count
        chotot_count  = poster.chotot_count
        chotot_mo_gioi_count  = poster.chotot_mo_gioi_count
        chotot_chinh_chu_count  = poster.chotot_chinh_chu_count
        
        
        poster_dict = self._thong_ke_co_hay_cc(bds_id__siteleech_id__id,bds_id__mat_tien_or_trich_dia_chi, site_post_count,count_post_all_site,
        address_topic_number, guess_count, dd_tin_cua_co_count, bds_id__dd_tin_cua_co, dd_tin_cua_dau_tu_count,
        bds_id__dd_tin_cua_dau_tu,chotot_count, chotot_mo_gioi_count, chotot_chinh_chu_count, bds_id__siteleech_id__name,
        bds_id__chotot_moi_gioi_hay_chinh_chu)
        poster.write(poster_dict)

        # if bds_id__mat_tien_or_trich_dia_chi:
        #     self.env['bds.address'].write_address_to_table(bds_id__mat_tien_or_trich_dia_chi, bds_id__siteleech_id__id, self.id, poster.id)



    #
    
        

               

