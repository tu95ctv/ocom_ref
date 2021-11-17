# -*- coding: utf-8 -*-
import re
import datetime
from datetime import timedelta
import os
import sys
import pytz
import traceback
from time import sleep
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)
from unidecode import unidecode
import json
import math
import re
from urllib import request
from unidecode import unidecode
import threading, multiprocessing
# from odoo.osv import expression
# from .compute_bds import _compute_mat_tien_or_trich_dia_chi1
import logging
_logger = logging.getLogger(__name__)

from odoo import models


#fetch_list -> để hiển thị ở chế độ test mode chạy run trong file py này
# ở module này sẽ tạo ra MainFetchCommon

#MainFetchCommon: có nhiều hàm chung cho các site, nhưng cũng có riêng cho chợ tốt

CHOTOT_CATE_CV = {'Căn hộ/Chung cư':'Căn hộ chung cư', 'Đất':'Các loại đất', 'Nhà ở':'Các loại nhà'}
class MainFetchCommon(models.AbstractModel):
    _name = 'abstract.main.fetch'
    is_save_ph = False
    allow_update = True
    set_attrs_dict_for_test = {}
    fets = {}
    # def __init__(self, set_attrs_dict_for_test = {}):
    #     self.set_attrs_dict_for_test = set_attrs_dict_for_test
    
    def file_from_tuong_doi(self, tuong_doi_path):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        # if self.fets['is_test']:
        dir_path = os.path.dirname(dir_path)
        # dir_path = os.path.dirname(dir_path)
    #     dir_path = r"C:\D4\tgl_code\bds12\bds\models"
        f = open(os.path.join(dir_path,'html_log', '%s.html'%tuong_doi_path), 'r', encoding="utf8")
        return f.read()
    
    def save_to_disk(self, ct, name_file ):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        dir_path = os.path.dirname(dir_path)
        # dir_path = os.path.dirname(dir_path)
        f = open(os.path.join(dir_path, 'html_log', '%s.html'%name_file), 'w', encoding="utf8")
        f.write(ct)
        f.close()

    def save_to_disk_mau( self, ct, page_or_topic, surfix='' ):
        if self.set_attrs_dict_for_test.get('is_save_mau'):
            dir_path = os.path.dirname(os.path.abspath(__file__))
            dir_path = os.path.dirname(dir_path)
            # dir_path = os.path.dirname(dir_path)
            f = open(os.path.join(dir_path, 'html_log', '%s_%s%s.html'%(page_or_topic, self.fets['site_name'], '_%s'%surfix if surfix else '')), 'w', encoding="utf8")
            f.write(ct)
            f.close()

    def get_main_obj(self):
        return self.env['bds.bds']
    
    def get_public_date_from_public_datetime(self, topic_data_from_page):
        public_datetime = topic_data_from_page['public_datetime'] # naitive datetime
        gmt7_public_datetime = convert_native_utc_datetime_to_gmt_7(public_datetime)
        public_date  = gmt7_public_datetime.date()
        return public_datetime, public_date

    #topic handle_bds_type_update_compare_price
    def th_bds_type_update_compare_price(self, search_bds_obj, topic_data_from_page):

        public_datetime = topic_data_from_page['public_datetime']
        public_date = topic_data_from_page['public_date']
        update_dict = {}
        now = datetime.datetime.now()
        diff_day_public_from_now =  (now - public_datetime).days
        if diff_day_public_from_now==0:
            public_datetime_cu  = search_bds_obj.public_datetime
            print ('**topic_data_from_page**', topic_data_from_page)
            print ('***public_datetime**', public_datetime, '**public_datetime_cu**', public_datetime_cu)
            diff_public_datetime_in_hours = int((public_datetime - public_datetime_cu + timedelta(hours=1)).seconds/3600)
            if diff_public_datetime_in_hours > 2 :
                public_date_cu =  search_bds_obj.public_date
                diff_public_date = (public_date - public_date_cu).days
                so_lan_diff_public_update = search_bds_obj.so_lan_diff_public_update + 1
                update_dict.update({
                    'public_datetime': public_datetime, 
                    # 'public_datetime_cu':public_datetime_cu,
                    'diff_public_datetime':diff_public_datetime_in_hours,
                    'public_date':public_date, 
                    # 'public_date_cu':public_date_cu,
                    'diff_public_date':diff_public_date, 
                    'so_lan_diff_public_update':so_lan_diff_public_update,
                    'publicdate_ids':[(0,False,{
                                'public_datetime': public_datetime, 
                                'public_datetime_cu':public_datetime_cu,
                                'diff_public_datetime':diff_public_datetime_in_hours,
                                'public_date':public_date, 
                                'public_date_cu':public_date_cu,
                                'diff_public_date':diff_public_date, 
                                }
                                )]
                    })
            gia=topic_data_from_page['price']
            gia_cu = search_bds_obj.price
            diff_gia = gia - gia_cu
            if diff_gia != 0.0:
                so_lan_gia_update = search_bds_obj.so_lan_gia_update + 1
                update_dict.update({
                    'so_lan_gia_update':so_lan_gia_update,
                    'ngay_update_gia':datetime.datetime.now(),
                    'diff_gia':diff_gia,
                    'gialines_ids':[(0,False,{'gia':gia, 'gia_cu':gia_cu, 'diff_gia':diff_gia})]
                    })
        return update_dict


    def th_more_create_dict(self, topic_data_from_page, url_id, link):
        create_dict = {}
       
        create_dict['siteleech_id'] = self.fets['siteleech_id_id']
        create_dict['cate'] = url_id.cate
        create_dict['sell_or_rent'] = url_id.sell_or_rent
        # create_dict['link'] = link
        create_dict['url_id'] = url_id.id
        
        return create_dict



    def get_or_create_quan_include_state(self, tinh_str, quan_str):
        tinh_str = re.sub('tp|Thành phố|tỉnh','', tinh_str, flags=re.I)
        tinh_str = tinh_str.strip()

        # if re.search('Hồ Chí Minh', tinh_str, re.I):
        #     tinh_str = 'Thành phố Hồ Chí Minh'
        # elif re.search('Hà Nội', tinh_str, re.I):
        #     tinh_str = 'Thủ đô Hà Nội'

        # elif not re.search('^tỉnh', tinh_str, re.I):
        #     tinh_str = 'Tỉnh ' + tinh_str
        if tinh_str:
            country_obj = self.env['res.country'].search([('name','ilike','viet')])[0]
            # state = g_or_c_ss(self.env['res.country.state'], {'name':tinh_str, 'country_id':country_obj.id},
            #                     {'code':tinh_str}, False)

            state = self.env['res.country.state'].search(['|',('name_without_prefix','=', tinh_str),
            ('name','=', tinh_str),('country_id','=', country_obj.id)])
            if not state:
                state = tinh_str
                quan = False
                return state, quan
                # raise UserError('Sao không có state')
            state = state[-1] if len(state)> 1 else state
            if quan_str:
                # quan = g_or_c_ss(self.env['res.country.district'], {'name':quan_str, 'state_id':state.id},
                #                     {}, False)
                quan = self.env['res.country.district'].search(['|',('name_without_prefix','=', quan_str),
                ('name','=', quan_str),('state_id','=', state.id)])
                if not quan:
                    quan = quan_str
                    return tinh_str, quan_str
                    # raise UserError('Sao không có quận')
            else:
                quan = False
            return state, quan
   

    def write_quan_phuong(self, topic_dict):
        update_dict = {}
        tinh = topic_dict['region_name']
        if not tinh:
            return False, False, False
        if 'area_name' in topic_dict:
            quan_name = topic_dict['area_name']
        else:
            quan_name = False
        state, quan = self.get_or_create_quan_include_state(tinh, quan_name)
        if isinstance(state, str):
            return state, quan, False
        print ('******88state, quan', state, quan)
        if quan:
            district_id = quan.id
        else:
            district_id = False
        if district_id:
            update_dict['district_id'] = district_id
            ward =  topic_dict.get('ward_name')
            if ward:
                ward_id = self.env['res.country.ward'].search(['|',('name_without_prefix','=', ward),
                ('name','=', ward),('district_id','=', district_id)])
                update_dict['ward_id'] = ward_id.id
                if not ward_id:
                    return state.name, quan.name, ward
       
        return update_dict

    def write_images(self, topic_dict):
        def create_or_get_one_in_m2m_value( url):
            url = url.strip()
            if url:
                return g_or_c_ss(self.env['bds.images'],{'url':url})
        update_dict = {}
        images_urls = topic_dict.get('images',[])
        if images_urls:
            object_m2m_list = list(map(create_or_get_one_in_m2m_value, images_urls))
            m2m_ids = list(map(lambda x:x.id, object_m2m_list))
            if m2m_ids:
                val = [(6, False, m2m_ids)]
                update_dict['images_ids'] = val
        return update_dict   

    def write_poster(self, topic_dict, siteleech_id_id):
        search_dict = {}
        phone = topic_dict['phone']
        search_dict['phone'] = phone 
        account_name = topic_dict['account_name']
        search_dict['login'] = str(phone)+'@gmail.com'
        poster =  self.env['bds.poster'].search([('phone','=', phone)])
        if poster:
            posternamelines_search_dict = {'username_in_site':account_name, 'site_id':siteleech_id_id, 'poster_id':poster.id}
            g_or_c_ss(self.env['bds.posternamelines'], posternamelines_search_dict)
                                                
        else:
            
            poster =  self.env['bds.poster'].create(search_dict)
            if siteleech_id_id:
                self.env['bds.posternamelines'].create( {'username_in_site':account_name, 'site_id':siteleech_id_id, 'poster_id':poster.id})
        return {'poster_id':poster.id}

    def convert_cate_id_name(self, site_name, loai_nha):
        
        if site_name == 'chotot':
            
            print ('kakaka',hex(id(CHOTOT_CATE_CV)))
            loai_nha = CHOTOT_CATE_CV.get(loai_nha, loai_nha)
        return loai_nha



    def write_cate_id(self, topic_dict, site_name):
        loai_nha = topic_dict['loai_nha']
        loai_nha = self.convert_cate_id_name(site_name, loai_nha)
        cate_id = g_or_c_ss(self.env['bds.cate'],{'name': loai_nha}, {'description':self.fets['site_name']})
        return {'cate_id':cate_id.id}


    def write_trich_dia_chi(self, topic_dict):
        html = topic_dict['html']
        mat_tien_address, trich_dia_chi, mat_tien_or_trich_dia_chi, is_mat_tien_or_trich_dia_chi = \
            _compute_mat_tien_or_trich_dia_chi1(self, html, html)
        topic_dict['mat_tien_address'] = mat_tien_address
        topic_dict['trich_dia_chi'] = trich_dia_chi
        topic_dict['mat_tien_or_trich_dia_chi'] = mat_tien_or_trich_dia_chi
        topic_dict['is_mat_tien_or_trich_dia_chi'] = is_mat_tien_or_trich_dia_chi
    
    def write_so_phong_ngu(self, topic_dict):
        html = topic_dict['html']
        if not html:
            return
        so_phong_ngu = _compute_so_phong_ngu(html)
        topic_dict['so_phong_ngu'] = so_phong_ngu

    def write_html_khong_dau(self, topic_dict):
        html = topic_dict['html']
        html_khong_dau = unidecode(html) if html else html
        topic_dict['html_khong_dau'] = html_khong_dau

    def write_loai_hem_combine(self, topic_dict):
        html = topic_dict['html']
        if not html:
            return
        mat_tien, full_mat_tien, is_mat_tien, hem_rong_char, hem_rong, full_loai_hem,\
        loai_hem_selection, loai_hem_combine = \
            _compute_loai_hem_combine(html)
        topic_dict['mat_tien'] = mat_tien
        topic_dict['full_mat_tien'] = full_mat_tien
        topic_dict['is_mat_tien'] = is_mat_tien
        topic_dict['hem_rong_char'] = hem_rong_char
        topic_dict['hem_rong'] = hem_rong
        topic_dict['loai_hem_selection'] = loai_hem_selection
        topic_dict['loai_hem_combine'] = loai_hem_combine

    def write_compute_kw_mg(self, topic_dict):
        html = topic_dict['html']
        if not html:
            return 
        kw_co_date, kw_mg_cap_2, is_kw_mg_cap_2, kw_co_special_break, kw_co_break,\
            hoa_la_canh, t1l1, kw_mg, dd_tin_cua_co = _compute_kw_mg(html)

        topic_dict['kw_co_date'] = kw_co_date
        topic_dict['kw_mg_cap_2'] = kw_mg_cap_2
        topic_dict['is_kw_mg_cap_2'] = is_kw_mg_cap_2
        topic_dict['kw_co_special_break'] = kw_co_special_break
        topic_dict['kw_co_break'] = kw_co_break
        topic_dict['hoa_la_canh'] = hoa_la_canh
        topic_dict['t1l1'] = t1l1
        topic_dict['kw_mg'] = kw_mg
        topic_dict['dd_tin_cua_co'] = dd_tin_cua_co

    def write_dd_tin_cua_dau_tu(self, topic_dict):
        html = topic_dict['html']
        kw_hoa_hong, kw_so_tien_hoa_hong, dd_tin_cua_dau_tu = _compute_dd_tin_cua_dau_tu(html)

        topic_dict['kw_hoa_hong'] = kw_hoa_hong
        topic_dict['kw_so_tien_hoa_hong'] = kw_so_tien_hoa_hong
        topic_dict['dd_tin_cua_dau_tu'] = dd_tin_cua_dau_tu

    def write_compute_choosed_area_muc_gia(self, topic_dict):
        html = topic_dict['html']
        gia = topic_dict['gia']
        if not self.fets['is_test']:
            print ('****topic_dict', topic_dict)
            district_id = topic_dict.get('district_id')
            if not district_id:
                return False

            district_id_obj = self.env['res.country.district'].browse(district_id)
        else:
            district_id_obj = False
        loai_hem_combine = topic_dict['loai_hem_combine']
        area = topic_dict['area']
        don_gia_quan, ti_le_don_gia_dat_con_lai, ti_le_don_gia, \
            auto_ngang, auto_doc, auto_dien_tich, ti_le_dien_tich_web_vs_auto_dien_tich, \
            dtsd, choose_area, so_lau, so_lau_char, so_lau_he_so,\
            dtsd_tu_so_lau, ti_le_dtsd, dtsd_combine, gia_xac_nha,\
            gia_dat_con_lai, don_gia_dat_con_lai, don_gia, muc_don_gia,\
            muc_ti_le_don_gia, muc_dt, muc_gia, ti_le_gia_dat_con_lai_gia = \
            _compute_choosed_area_muc_gia(html, gia, area, district_id_obj, loai_hem_combine)
        topic_dict['don_gia_quan'] = don_gia_quan
        topic_dict['ti_le_don_gia_dat_con_lai'] = ti_le_don_gia_dat_con_lai
        topic_dict['ti_le_don_gia'] = ti_le_don_gia
        topic_dict['auto_ngang'] = auto_ngang
        topic_dict['auto_doc'] = auto_doc
        topic_dict['auto_dien_tich'] = auto_dien_tich

        topic_dict['ti_le_dien_tich_web_vs_auto_dien_tich'] = ti_le_dien_tich_web_vs_auto_dien_tich
        topic_dict['dtsd'] = dtsd
        topic_dict['choose_area'] = choose_area
        topic_dict['so_lau'] = so_lau
        topic_dict['so_lau_char'] = so_lau_char
        topic_dict['so_lau_he_so'] = so_lau_he_so

        topic_dict['dtsd_tu_so_lau'] = dtsd_tu_so_lau
        topic_dict['ti_le_dtsd'] = ti_le_dtsd
        topic_dict['dtsd_combine'] = dtsd_combine
        topic_dict['gia_xac_nha'] = gia_xac_nha
        topic_dict['gia_dat_con_lai'] = gia_dat_con_lai
        topic_dict['don_gia_dat_con_lai'] = don_gia_dat_con_lai

        topic_dict['don_gia'] = don_gia
        topic_dict['muc_don_gia'] = muc_don_gia
        topic_dict['muc_ti_le_don_gia'] = muc_ti_le_don_gia
        topic_dict['muc_dt'] = muc_dt
        topic_dict['muc_gia'] = muc_gia
        topic_dict['ti_le_gia_dat_con_lai_gia'] = ti_le_gia_dat_con_lai_gia
    #kaka xem cái này nằm đâu
    def odoo_model_topic_dict(self, topic_dict):
        if not self.fets['is_test']:
            rs = self.write_quan_phuong(topic_dict)
            if isinstance(rs, dict):
                topic_dict.update(rs)
            else:
                print ('****không tìm thấy quận rs****', rs)
                topic_dict.update({'state_district_ward_nok': ','.join([str(i) for i in rs])})
            topic_dict.update(self.write_images(topic_dict))
            topic_dict.update(self.write_poster(topic_dict, self.fets['siteleech_id_id']))
            topic_dict.update(self.write_cate_id(topic_dict, self.fets['site_name']))
        
        topic_dict.update(write_gia(topic_dict))
        topic_dict.update(write_public_datetime(topic_dict))
        self.write_trich_dia_chi(topic_dict)
        self.write_html_khong_dau(topic_dict)
        self.write_so_phong_ngu(topic_dict)
        self.write_loai_hem_combine(topic_dict)
        self.write_compute_kw_mg(topic_dict)
        self.write_dd_tin_cua_dau_tu(topic_dict) 
        self.write_compute_choosed_area_muc_gia(topic_dict)

    def request_and_parse_html_topic(self, link):
        print ('*********request_and_parse_html_topic'*10,'link', link )
        if not link:
            topic_dict = {}
            # topic_dict['link'] = None 
            return topic_dict
        if self.fets.get('topic_path'):
            topic_html = self.file_from_tuong_doi(self.fets['topic_path'])
        else:
            headers = self.page_header_request()
            header_kwargs = {'headers': headers} if headers else {}
            topic_html = request_html(link, **header_kwargs)
        
        if self.fets.get('topic_count'):
            self.save_to_disk_mau(topic_html, 'topic', surfix='')
        try:
            # is_save_and_raise_in_topic = self.set_attrs_dict_for_test.get('is_save_and_raise_in_topic')
            # if is_save_and_raise_in_topic:
            #     raise SaveAndRaiseException(self.fets['site_name'])
            topic_dict = self.parse_html_topic(topic_html)
        except SaveAndRaiseException as e:
            self.save_to_disk(topic_html, 'file_topic_bug_theo_y_muon_%s'%str(e))
            raise
        except SaveAndPass as e:
            self.save_to_disk(topic_html, 'file_topic_bug_save_and_pass_%s'%str(e))
            raise
        except:
            self.save_to_disk(topic_html, 'file_topic_bug')
            raise
        topic_dict['link'] = link
        return topic_dict


    def del_list_id_topic_data_from_page(self, topic_data_from_page):
        if 'list_id' in topic_data_from_page:
            del topic_data_from_page['list_id']

    def get_search_domain(self, link, topic_data_from_page):
        return [('link','=',link)]


    #kakak link lấy từ đâu ra
    def topic_handle(self, link, url_id, topic_data_from_page, search_bds_obj=None):
        a_topic_fetch_dict = {}
        create_dict = {}
        self.fets['link'] = link
        self.fets['page_dict'] = topic_data_from_page
        if not self.fets['is_test']:
            if not search_bds_obj:
                Main_obj = self.get_main_obj()
                #kaka sửa cái này lại thành search kiểu gì
                domain = self.get_search_domain(link, topic_data_from_page)
                search_bds_obj= Main_obj.search(domain)
            else:
                link = search_bds_obj.link
        is_fail_link_number = 0
        is_existing_link_number = 0
        is_update_link_number = 0
        is_create_link_number = 0
        try:
            if not self.fets['is_test'] and search_bds_obj:
                if not self.fets['is_force_update_topic_combine']:# update ở mode bình thường, is_force_update_topic_combine: là gì
                    update_dict = {}
                    if self.fets['st_is_bds_site']: # thế đéo nào là st_is_bds_site
                        topic_data_from_page.update(write_public_datetime(topic_data_from_page))
                        topic_data_from_page.update(write_gia(topic_data_from_page))
                        compare_update_dict = self.th_bds_type_update_compare_price(search_bds_obj, topic_data_from_page)
                        update_dict.update(compare_update_dict)
                    a_topic_fetch_dict = topic_data_from_page
                else:
                    update_dict = self.request_and_parse_html_topic(link)
                    update_dict.update(topic_data_from_page)
                    if self.fets['st_is_bds_site']:
                        self.odoo_model_topic_dict(update_dict)

                    if self.fets['model_id']:
                        update_dict['is_full_topic'] =  True
                    a_topic_fetch_dict = update_dict

                if update_dict:
                    search_bds_obj.write(update_dict)
                    is_update_link_number = 1

                is_existing_link_number = 1
            else:
                link = topic_data_from_page.get('link')
                create_dict = {}
                # coi cái st_is_request_topic là gì kaka
                if self.fets['st_is_request_topic'] and link:
                    create_dict = self.request_and_parse_html_topic(link)
                if self.fets['is_pagehandle']:
                    print ('**** vào đây khoong topic_data_from_page***'*10, topic_data_from_page)
                    create_dict.update(topic_data_from_page)
                # more_from_page = self.more_from_page(topic_data_from_page)
                # create_dict.update(more_from_page)
                if self.fets['st_is_bds_site'] :
                    self.odoo_model_topic_dict(create_dict)
                    if not self.fets['is_test']:
                        more_create_dict = self.th_more_create_dict(create_dict, url_id, link)
                        create_dict.update(more_create_dict)
                a_topic_fetch_dict = create_dict
                del_f = []
                for f,v in create_dict.items():
                    if f not in Main_obj._fields:
                        del_f.append(f)
                    else:
                        if isinstance(v,dict):
                            print ('aafsafdsdfsadfsad', v)
                            print (abc)
                for f in del_f:
                    del create_dict[f]
                print ('*************88create_dict***********', create_dict)
                if not self.fets['is_test']:
                    Main_obj.create(create_dict) 
                    # self.env.cr.commit()
                is_create_link_number = 1
                if not self.fets['is_test']:
                    self.env['bds.error'].create({
                    'name':'success link',
                    'des':'success link',
                    'link':link,
                    'type':'success',
                    'link_type':'topic',
                    'fetch_item_id':self.fets['fetch_item_id'].id,
                    'error_or_success':'success',
                        })
                    

        except FetchError as e:
            is_fail_link_number = 1
            if not self.fets['is_test']:
                self.env['bds.error'].create({
                    'name':str(e),
                    'des':str(e),
                    'link':link,
                    'type':'fetch_error',
                    'link_type':'topic',
                    'fetch_item_id':self.fets['fetch_item_id'].id,
                    }
                )

           
        except:
            raise
            # is_fail_link_number = 1
            # self.env['bds.error'].create({
            #     'name':'internal_error',
            #     'des':str(traceback.format_exc()),
            #     'link':link,
            #     'type':'internal_error',
            #     'link_type':'topic',
            #     'fetch_item_id':self.fets['fetch_item_id'].id,
            #     }
            #     )
        return is_existing_link_number, is_update_link_number, is_create_link_number, is_fail_link_number, a_topic_fetch_dict

        


    def make_topic_link_from_list_id_common(self, list_id):
        link = list_id
        return link  

    def page_header_request(self):
        return None

    # sinh ra topic_data_from_pages_of_a_page và lập trong đó để lấy từng topic
    def page_handle(self, page_int,url, url_id, fetch_item_id):
        existing_link_number, update_link_number, create_link_number, fail_link_number, link_number = 0, 0, 0, 0, 0
        page_list = []
        try:
            if not self.fets['page_path']:
                format_page_url = url or  url_id.url 
                page_url = self.create_page_link(format_page_url, page_int)
                headers = self.page_header_request()
                header_kwargs = {'headers': headers} if headers else {}
                html_page = request_html(page_url,**header_kwargs)
            else:
                html_page = self.file_from_tuong_doi(self.fets['page_path'])
            self.save_to_disk_mau(html_page, 'page', surfix='')
            try:
                topic_data_from_pages_of_a_page = self.ph_parse_pre_topic(html_page)
            except SaveAndRaiseException as e:
                self.save_to_disk(html_page, 'file_topic_bug_theo_y_muon_%s'%str(e))
                raise
                # raise 
            except:
                file_name = 'file_page_bug' if not self.fets['page_path'] else 'file_page_bug_page_path'
                self.save_to_disk(html_page, file_name)
                raise
        except FetchError as e:
            self.env['bds.error'].create({
                'name':str(e),
                'des':str(e),
                'link':page_url,
                'type':'fetch_error',
                'link_type':'page',
                'fetch_item_id':fetch_item_id.id,
                }
            )
            return existing_link_number, update_link_number, create_link_number, fail_link_number, link_number
        except Exception as e:
            raise
        if not topic_data_from_pages_of_a_page:
            file_name = 'file_page_bug_no_topic' if not self.fets['page_path'] else 'file_page_bug_page_path'
            self.save_to_disk(html_page, file_name)
            raise ValueError('topic_data_from_pages_of_a_page is empty')
         
        for topic_count, topic_data_from_page in enumerate(topic_data_from_pages_of_a_page):
            self.fets['topic_count'] = topic_count
            link = topic_data_from_page.get('link')
            try:
                is_existing_link_number, is_update_link_number, is_create_link_number, is_fail_link_number,  a_topic_fetch_dict = \
                    self.topic_handle(link, url_id, topic_data_from_page
                            )
                # self._cr.commit()
                existing_link_number += is_existing_link_number
                update_link_number += is_update_link_number
                create_link_number += is_create_link_number
                fail_link_number +=is_fail_link_number
                page_list.append(a_topic_fetch_dict)
                
            except SaveAndPass:
                pass

        link_number = len(topic_data_from_pages_of_a_page)
        return existing_link_number, update_link_number, create_link_number, fail_link_number, link_number, page_list

    def gen_page_number_list(self, fetch_item_id ): 
        if self.fets['is_test']:
            end_page_number_in_once_fetch, page_lists, begin, number_of_pages = 1,[1],1,1
            return end_page_number_in_once_fetch, page_lists, begin, number_of_pages
        url_id = fetch_item_id
        set_number_of_page_once_fetch_name = 'set_number_of_page_once_fetch'
        set_leech_max_page_name = 'set_leech_max_page'
        current_page = fetch_item_id.current_page
        set_number_of_page_once_fetch = getattr(url_id, set_number_of_page_once_fetch_name)
        url_set_leech_max_page = getattr(url_id, set_leech_max_page_name)
        set_leech_max_page = self.max_page or url_set_leech_max_page
        fetch_error = False
        try:
            web_last_page_number =  self.get_last_page_number(fetch_item_id.url_id)
            fetch_item_id.url_id.write({'web_last_page_number':web_last_page_number})
        except FetchError as e:
            web_last_page_number = fetch_item_id.url_id.web_last_page_number or 200
            fetch_error = True

        if set_leech_max_page and  set_leech_max_page < web_last_page_number:
            max_page =  set_leech_max_page
        else:
            max_page = web_last_page_number
        begin = current_page + 1
        min_page = url_id.min_page or 1
        if begin < min_page:
            begin = min_page
        if begin > max_page:
            begin  = min_page
        end = begin   + set_number_of_page_once_fetch - 1
        if end > max_page:
            end = max_page
        end_page_number_in_once_fetch = end
        page_lists = range(begin, end + 1)
        number_of_pages = end - begin + 1
        return end_page_number_in_once_fetch, page_lists, begin, number_of_pages, max_page


    def fetch_bo_sung_da_co_link(self, fetch_item_id):
        model = fetch_item_id.model_id.name
        objs = self.env[model].search([('is_full_topic','=',False)], limit=fetch_item_id.limit)
        existing_link_number, update_link_number, create_link_number, link_number, fail_link_number = 0,0,0,0,0
        for r in objs:
            url_id = False
            try:
                topic_data_from_page = {}
                    
                link = None
                is_fail_link_number, is_existing_link_number, is_update_link_number, is_create_link_number, create_dict= \
                    self.topic_handle(link, url_id, topic_data_from_page, search_bds_obj=r)
                existing_link_number += is_existing_link_number
                update_link_number += is_update_link_number
                create_link_number += is_create_link_number
                fail_link_number += is_fail_link_number
                link_number += 1
            except FetchError as e:
                self.env['bds.error'].create({'name':str(e),'des':str(e)})
        return existing_link_number, update_link_number, create_link_number, link_number, fail_link_number


    def get_st_is_bds_site(self):
        return True


    def setting_for_fetch_obj(self, url_id, fetch_item_id):
        self.fets['siteleech_id_id'] = url_id.siteleech_id.id  if url_id else False
        
        if url_id.sell_or_rent =='duan':
            sitename = url_id.siteleech_id.name + '_duan'
        else:
            sitename = url_id.siteleech_id.name

        self.fets['site_name'] = ( sitename + (' ' + url_id.fetch_mode if url_id.fetch_mode else '')) if url_id else self.set_attrs_dict_for_test.get('site_name')
        
        
        self.fets['model_name'] = fetch_item_id.model_id.name if fetch_item_id else False
        self.fets['st_is_bds_site'] = self.get_st_is_bds_site()
        self.fets['st_is_request_topic'] = not fetch_item_id.not_request_topic if fetch_item_id else self.set_attrs_dict_for_test.get('st_is_request_topic', True)
        self.fets['model_id'] = fetch_item_id.model_id if fetch_item_id else False
        self.fets['topic_link'] = fetch_item_id.topic_link if fetch_item_id else self.set_attrs_dict_for_test.get('topic_link')
        self.fets['topic_path'] = fetch_item_id.topic_path if fetch_item_id else self.set_attrs_dict_for_test.get('topic_path')
        self.fets['page_path'] = fetch_item_id.page_path if fetch_item_id else self.set_attrs_dict_for_test.get('page_path')
        self.fets['is_must_update_topic'] = fetch_item_id.page_path if fetch_item_id else False
        self.fets['is_pagehandle'] = not (self.fets['topic_link'] or self.fets['topic_path'] or \
                    self.fets['model_id'])
        self.fets['is_test'] = self.set_attrs_dict_for_test.get('is_test')
        self.fets['url'] = url_id.url if url_id else self.set_attrs_dict_for_test.get('url')
        

    def _fetch_a_url_id (self,url_id, fetch_item_id):
        fetch_list = []
        end_page_number_in_once_fetch = False
        existing_link_number, update_link_number, create_link_number, link_number, fail_link_number = 0, 0, 0, 0, 0
        if self.fets['topic_link'] or self.fets['topic_path']:
            topic_data_from_page = {}
            existing_link_number_one_page, update_link_number_one_page, create_link_number_one_page,\
                    fail_link_number_one_page, fetch_dict = \
                self.topic_handle(self.fets['topic_link'], url_id, topic_data_from_page)
            link_number_one_page = 1
            existing_link_number += existing_link_number_one_page
            update_link_number += update_link_number_one_page
            create_link_number += create_link_number_one_page
            fail_link_number += fail_link_number_one_page
            link_number += link_number_one_page
            is_finished = False
            fetch_list.append(fetch_dict)
        elif self.fets['model_id']:
            existing_link_number, update_link_number, create_link_number, link_number, fail_link_number = \
                self.fetch_bo_sung_da_co_link(fetch_item_id)
            link_number = update_link_number
            is_finished = False
        else:
            if not self.fets['page_path'] and fetch_item_id:
                end_page_number_in_once_fetch, page_lists, begin, so_page, max_page =  self.gen_page_number_list(fetch_item_id) 
            else: 
                if not self.fets['page_path']:
                    begin_page, end_page = self.set_attrs_dict_for_test.get('begin_page') or 1, self.set_attrs_dict_for_test.get('end_page') or 1
                else:
                    begin_page, end_page = 1,1
                page_lists = range(begin_page, end_page+1)
            
            for page_int in page_lists:
                rs = self.page_handle( page_int, self.fets['url'], url_id, fetch_item_id)

                existing_link_number_one_page, update_link_number_one_page, create_link_number_one_page,\
                    fail_link_number_one_page, link_number_one_page, page_list = rs
                    
                existing_link_number += existing_link_number_one_page
                update_link_number += update_link_number_one_page
                create_link_number += create_link_number_one_page
                fail_link_number += fail_link_number_one_page
                link_number += link_number_one_page
                if not self.fets['page_path'] and not self.fets['is_test']:
                    if end_page_number_in_once_fetch == max_page:
                        is_finished = True
                    else:
                        is_finished = False
                else:
                    is_finished = True
                fetch_list.extend(page_list)
        return existing_link_number, update_link_number, create_link_number, link_number, fail_link_number, is_finished, end_page_number_in_once_fetch, fetch_list


    def fetch_a_url_id (self, fetch_item_id):
        begin_time = datetime.datetime.now()
        if fetch_item_id:
            url_id = fetch_item_id.url_id
        else:
            url_id = False
        self.setting_for_fetch_obj( url_id, fetch_item_id)
        
        self.fets['is_force_update_topic_combine'] = self.fets['topic_link'] or self.fets['topic_path'] \
                     or self.fets['is_must_update_topic'] or bool(self.fets['model_id'])
        self.fets['fetch_item_id'] = fetch_item_id


        existing_link_number, update_link_number, create_link_number, link_number, fail_link_number, is_finished,\
            end_page_number_in_once_fetch, fetch_list = \
            self._fetch_a_url_id (url_id, fetch_item_id)
        interval = (datetime.datetime.now() - begin_time).total_seconds()
        if not self.fets['is_test']:
            self.write_fetch(fetch_item_id, interval, end_page_number_in_once_fetch, create_link_number,\
            update_link_number, link_number, fail_link_number, existing_link_number, is_finished)
            self.ph_fetch_item_history_deal(fetch_item_id, end_page_number_in_once_fetch, create_link_number,\
            update_link_number, link_number, existing_link_number, interval)
            self.last_fetched_item_id = fetch_item_id
        return fetch_list

    def write_fetch(self, fetch_item_id, interval, end_page_number_in_once_fetch, create_link_number,\
        update_link_number, link_number, fail_link_number, existing_link_number, is_finished):
        fetch_item_id.fetched_number +=1
        fetch_item_id.interval = interval
        fetch_item_id.write({'current_page': end_page_number_in_once_fetch,
                    'create_link_number': create_link_number,
                    'update_link_number': update_link_number,
                    'link_number': link_number,
                    'fail_link_number':fail_link_number, 
                    'existing_link_number': existing_link_number,
                    'is_finished':is_finished,
                    })

    def ph_fetch_item_history_deal(self, fetch_item_id, end_page_number_in_once_fetch, create_link_number,\
        update_link_number, link_number, existing_link_number, interval):
        can_xoa = self.env['bds.fetch.item.history'].search([('fetch_item_id','=', fetch_item_id.id)], offset=4)
        can_xoa.unlink()
        self.env['bds.fetch.item.history'].create({
            'current_page': end_page_number_in_once_fetch,
            'create_link_number': create_link_number,
            'update_link_number': update_link_number,
            'link_number': link_number,
            'existing_link_number': existing_link_number,
            'fetch_item_id':fetch_item_id.id,
            'interval':interval,
        })

    def look_next_fetched_url_id(self):
        fetch_item_ids = self.fetch_item_ids.filtered(lambda i: not i.disible)
        if self.is_next_if_only_finish:
            object_url_ids = fetch_item_ids.filtered(lambda r: not r.is_finished)
        else:
            object_url_ids = fetch_item_ids
        current_fetched_url_id = self.last_fetched_item_id
        if not current_fetched_url_id.model_id:
            if current_fetched_url_id not in fetch_item_ids:
                current_fetched_url_id = False
            if current_fetched_url_id and self.is_next_if_only_finish:
                if not current_fetched_url_id.is_finished:
                    return current_fetched_url_id
            if not object_url_ids and self.is_next_if_only_finish:
                object_url_ids.write({'is_finished':False})
        # tuần tự
        filtered_object_url_ids_id = object_url_ids.ids
        
        if not self.last_fetched_item_id.id:
            new_index = 0
        else:
            try:
                index_of_last_fetched_url_id = filtered_object_url_ids_id.index(self.last_fetched_item_id.id)
                new_index =  index_of_last_fetched_url_id + 1
            except ValueError:
                new_index = 0
            if new_index == len(filtered_object_url_ids_id):
                new_index = 0
        try:
            url_id = object_url_ids[new_index]
        except:
            raise ValueError('Không loop được url')
        return url_id

    # làm gọn lại ngày 23/02
    def fetch (self):
            # while 1:
                # sleep_count = 5
                # while sleep_count:
                #     print ('sleep....%s'%sleep_count)
                #     sleep(1)
                #     sleep_count-=1
            url_id = self.look_next_fetched_url_id()
            try:
                self.fetch_a_url_id(url_id)
            except FetchError as e:
                self.env['bds.error'].create({'name':str(e),'des':'type of error:%s'%type(e)})


    def fetch_all_url(self):
        url_ids = self.fetch_item_ids
        for url_id in url_ids:
            self.fetch_a_url_id (url_id)

    ########## cho tot###############

    def ph_parse_pre_topic(self, html_page):

        if self.is_save_ph:
            self.save_to_disk(html_page, 'page_%s'%'test_page')
            print (abc)
        topic_data_from_pages_of_a_page = []
        if self.fets['site_name'] == 'chotot':
            json_a_page = json.loads(html_page)
            topic_data_from_pages_of_a_page_origin = json_a_page['ads']
            for ad in topic_data_from_pages_of_a_page_origin:
                print ('**ad***', ad)
                topic_data_from_page = {}
                topic_data_from_page['price_string'] = ad.get('price_string')
                topic_data_from_page['price'] = ad.get('price',0)
                topic_data_from_page['gia'] = ad.get('price',0)/1000000000
                topic_data_from_page['date'] = ad['date']
                topic_data_from_page['link'] = self.make_topic_link_from_list_id(ad['list_id'])
                topic_data_from_page['html'] = ad.get('body','')
                topic_data_from_page['title']= ad['subject']
                topic_data_from_page['region_name'] = ad.get('region_name',False)
                topic_data_from_page['area_name'] = ad.get('area_name',False)
                try:
                    topic_data_from_page['ward_name'] = ad['ward_name']
                except:
                    pass
                
                if 'image' in ad:
                    topic_data_from_page['thumb'] = ad['image']
                if 'company_ad' in ad:
                    company_ad = ad['company_ad']
                else:
                    company_ad = False 
                topic_data_from_page['chotot_moi_gioi_hay_chinh_chu'] = \
                'moi_gioi' if company_ad else 'chinh_chu' 
                if 'category_name' in ad:
                    category_name = ad['category_name']
                    topic_data_from_page['loai_nha'] =  category_name
                else:
                    topic_data_from_page['loai_nha'] =  False
                topic_data_from_pages_of_a_page.append(topic_data_from_page)
        return topic_data_from_pages_of_a_page

    def create_page_link(self, format_page_url, page_int):
        if self.fets['site_name'] == 'chotot':
            url =  create_cho_tot_page_link(format_page_url, page_int)
            return url

    def parse_html_topic (self, topic_html):
        if self.fets['site_name'] =='chotot':
            topic_dict = self.get_topic_chotot(topic_html, self.fets['page_dict'])
            return topic_dict
        return super().parse_html_topic(topic_html)

    def make_topic_link_from_list_id(self, list_id):
        if  self.fets['site_name'] =='chotot':
            link  = 'https://gateway.chotot.com/v1/public/ad-listing/' + str(list_id)
            return link
        return self.make_topic_link_from_list_id_common(list_id)

    def get_last_page_number(self, url_id):
        if self.fets['site_name'] =='chotot':
            page_1st_url = create_cho_tot_page_link(url_id.url, 1)
            html = request_html(page_1st_url)
            html = json.loads(html)
            total = int(html["total"])
            web_last_page_number = int(math.ceil(total/20.0))
            return web_last_page_number
    
    def get_topic_chotot(self, topic_html, page_dict):
        update_dict = {}
        
        topic_html = json.loads(topic_html) 
        ad = topic_html['ad']
        ad_params = topic_html['ad_params']

        update_dict['region_name'] = ad.get('region_name',False)
        update_dict['area_name'] = ad.get('area_name')
        try:
            update_dict['ward_name'] = ad['ward_name']
        except:
            pass
        update_dict['images']= ad.get('images',[])
        update_dict['phone'] = ad['phone']
        update_dict['account_name'] = ad['account_name']
        update_dict['price_string'] = ad.get('price_string')
        update_dict['price'] = ad.get('price')
        update_dict['date'] = ad.get('date')
        address = ad_params.get('address',{}).get('value',False)
        if address:
            update_dict['address'] = address
        else:
            pass
        try:
            if not 'html' in page_dict:
                update_dict['html'] = ad.get('body','')
        except KeyError:
            pass
        update_dict['area']= ad.get('size',0)
        if 'title' not in page_dict:
            update_dict['title']= ad['subject']
        return update_dict

########## fetch tools####################
class FetchError(Exception):
    pass

class SaveAndRaiseException(Exception):
    pass

class SaveAndPass(Exception):
    pass

def g_or_c_ss(self_env_class_name,search_dict,
                create_write_dict ={},
                force_update=False,
                is_up_date = True,
                not_active_include_search = False
            ):
    if not_active_include_search:
        domain_not_active = ['|',('active','=',True),('active','=',False)]
    else:
        domain_not_active = []
    domain = []
    for i in search_dict:
        tuple_in = (i,'=',search_dict[i])
        domain.append(tuple_in)
    # domain = expression.AND([domain_not_active, domain])
    domain_not_active.extend(domain)
    domain = domain_not_active
    searched_object  = self_env_class_name.search(domain)
    if not searched_object:
        search_dict.update(create_write_dict)
        created_object = self_env_class_name.create(search_dict)
        return_obj =  created_object
    else:
        return_obj = searched_object
        is_change = force_update
        if not is_change and is_up_date:
            for attr in create_write_dict:
                domain_val = create_write_dict[attr]
                exit_val = getattr(searched_object,attr)
                try:
                    exit_val = getattr(exit_val,'id',exit_val)
                    if exit_val ==None: #recorderset.id ==None when recorder sset = ()
                        exit_val=False
                except:#singelton
                    pass
                # if isinstance(domain_val, datetime.date):
                #     exit_val = fields.Date.from_string(exit_val)
                if exit_val !=domain_val:
                    is_change = True
                    break
        if is_change:
            searched_object.write(create_write_dict)
    return return_obj       


headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36' }
def request_html(url, try_again=1, is_decode_utf8 = True, headers=headers):
    _logger.warning('***request_html***' + url)
    count_fail = 0
    def in_try():
        req =request.Request(url, None, headers)
        rp= request.urlopen(req)
        mybytes = rp.read()
        if is_decode_utf8:
            html = mybytes.decode("utf8")
            return html
        else:
            return mybytes
    while 1:
        if not try_again:
            return in_try()
        try:
            html = in_try()
            return html
        except Exception as e:
            print ('loi html')
            count_fail +=1
            sleep(5)
            if count_fail ==5:
                raise FetchError(u'Lỗi get html, url: %s'%url)
##############! fetch tools ########################
def create_cho_tot_page_link(url_input, page_int):
    repl = 'o=%s'%(20*(page_int-1))
    url_input,count = re.subn('o=\d+', repl, url_input)
    if not count:
        url_input += '&'+ repl
    if '&page=' not in url_input: 
        url_input = url_input +  '&page=' +str(page_int)
    else:
        repl = 'page=' +str(page_int)
        url_input = re.sub('page=\d+', repl, url_input)
    return url_input

def convert_native_utc_datetime_to_gmt_7(utc_datetime_inputs):
        local = pytz.timezone('Etc/GMT-7')
        utc_tz =pytz.utc
        gio_bat_dau_utc_native = utc_datetime_inputs
        gio_bat_dau_utc = utc_tz.localize(gio_bat_dau_utc_native, is_dst=None)
        gio_bat_dau_vn = gio_bat_dau_utc.astimezone (local)
        return gio_bat_dau_vn

ty_trieu_nghin_look = {'tỷ':1000000000, 'triệu':1000000, 'nghìn':1000, 'đ':1}     
def convert_gia_from_string_to_float(gia):# 3.5 triệu/tháng
    gia_ty, trieu_gia, price, thang_m2_hay_m2 = False, False, False, False
    gia = gia.strip()
    if not gia:
        return gia_ty, trieu_gia, price, thang_m2_hay_m2

    if re.search('thỏa thuận', gia, re.I):
        return gia_ty, trieu_gia, price, thang_m2_hay_m2

    try:
        rs = re.search('([\d\,\.]*) (\w+)(?:$|/)(.*$)', gia)
        gia_char = rs.group(1).strip()
        if not gia_char:
            return gia_ty, trieu_gia, price, thang_m2_hay_m2
        gia_char = gia_char.replace(',','.')
        ty_trieu_nghin = rs.group(2)
        thang_m2_hay_m2 = rs.group(3)
        if ty_trieu_nghin == 'đ':
            gia_char = gia_char.replace('.','')
        gia_float = float(gia_char)
        he_so = ty_trieu_nghin_look[ty_trieu_nghin]
        price = gia_float* he_so
        gia_ty = price/1000000000
        trieu_gia = price/1000000

    except:
        print ('exception gia', gia)
        raise
        
    return gia_ty, trieu_gia, price, thang_m2_hay_m2

MAP_CHOTOT_DATE_TYPE_WITH_TIMEDELTA = {
        u'ngày':'days',
        u'tuần':'weeks',
        u'hôm qua':'days',
        u'giờ':'hours',
        u'phút':'minutes',
        u'giây':'seconds',
        u'năm':'years',
        u'tháng':'months'
        }
        
def convert_chotot_date_to_datetime(string):
    rs = re.search (r'(\d*?)\s?(ngày|tuần|hôm qua|giờ|phút|giây|năm|tháng)',string,re.I)
    rs1 =rs.group(1)
    rs2 =rs.group(2)
    if rs1=='':
        rs1 =1
    rs1 = int (rs1)
    rs2 = MAP_CHOTOT_DATE_TYPE_WITH_TIMEDELTA[rs2]
    dt = datetime.datetime.now() - relativedelta(**{rs2:rs1})
    return dt

def write_gia(topic_dict):
        gia_dict = {}
        price_string = topic_dict.get('price_string',False)
        if price_string:
            gia_ty, trieu_gia, price, price_unit = convert_gia_from_string_to_float(price_string)
        else:
            gia_ty, trieu_gia, price, price_unit= False,False,False,False
        
        gia_dict['price_unit'] = price_unit # tháng/m2
        price = topic_dict.get('price', price)
        
        if price:
            gia_ty, gia_trieu = price/1000000000, price/1000000
        else:
            gia_ty, gia_trieu = False, False
        gia_dict['gia'] = gia_ty
        gia_dict['gia_trieu'] = gia_trieu
        gia_dict['price'] = price
        return gia_dict

def write_public_datetime(topic_dict):
    update = {}
    if 'date' in topic_dict and 'public_datetime' not in topic_dict:
        date = topic_dict['date']
        public_datetime = convert_chotot_date_to_datetime(date)
        update ['public_datetime'] = public_datetime
    if 'publish_date_str' in topic_dict and 'public_datetime' not in topic_dict:
        publish_date_str = topic_dict['publish_date_str']
        public_datetime = datetime.datetime.strptime(publish_date_str,"%d/%m/%Y")
        update ['public_datetime'] = public_datetime
        

    public_datetime = topic_dict.get('public_datetime')  or public_datetime # naitive datetime
    gmt7_public_datetime = convert_native_utc_datetime_to_gmt_7(public_datetime)
    public_date  = gmt7_public_datetime.date()
    # return public_datetime, public_date
    update['public_date'] = public_date
    update['public_datetime'] = public_datetime
    return update


#######################BDSCOMVN###################


header = {
                'Host': 'batdongsan.com.vn',
                #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                # 'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://batdongsan.com.vn/ban-nha-dat-tp-hcm/p4',
                'Connection': 'keep-alive',
                'Cookie': 'SERVERNAME=L_22006251500; _gcl_au=1.1.271490124.1593699646; __cfduid=d962388d50425a164b6fa007bb18400a11593699656; _ga=GA1.3.2004129680.1593699653; usidtb=el2cCH0hYkeyFsUCXtus4pJnBJX0iIA5; __auc=fc627e9a1730fe6dc02b1aad644; ins-storage-version=75; c_u_id=104601; uitb=%7B%22name%22%3A%22Nguyen%20Duc%20Tu%22%2C%22email%22%3A%22nguyenductu%40gmail.com%22%2C%22mobile%22%3A%220916022787%22%2C%22time%22%3A1593701739318%7D; NPS_b514e4e7_last_seen=1593701743389; _fbp=fb.2.1593701744644.54625863; _ym_uid=15937017471040494592; _ym_d=1593701747; __zi=2000.SSZzejyD6jy_Zl2jp1eKttQU_gxC3nMGTChWuC8NLyncmFxoW0L1t2AVkF62JGtQ8fgnzeP5IDidclhqXafDtIkV_FG.1; fpsend=147621; __zlcmid=yzjFnky3OLinOV; SERVERID=H; ASP.NET_SessionId=pmzli2x4f0m2fw0jfdbp2aov; _gid=GA1.3.1740494310.1594452137; psortfilter=1%24all%24VOE%2FWO8MpO1adIX%2BwMGNUA%3D%3D; sidtb=Xs6HBrUnnCvh6iGaEMGmhBx2nCLrUMGh; __asc=b0a63b421733d08f828fd8fa4e2',
                'Cookie': 'SERVERNAME=L_22006251500; _gcl_au=1.1.271490124.1593699646; __cfduid=d334ee9afa89db62b58be8d07341be0151598182301; _ga=GA1.3.2004129680.1593699653; usidtb=el2cCH0hYkeyFsUCXtus4pJnBJX0iIA5; __auc=fc627e9a1730fe6dc02b1aad644; ins-storage-version=75; c_u_id=104601; uitb=%7B%22name%22%3A%22Nguyen%20Duc%20Tu%22%2C%22email%22%3A%22nguyenductu%40gmail.com%22%2C%22mobile%22%3A%220916022787%22%2C%22time%22%3A1593701739318%7D; NPS_b514e4e7_last_seen=1593701743389; _fbp=fb.2.1593701744644.54625863; _ym_uid=15937017471040494592; _ym_d=1593701747; __zi=2000.SSZzejyD6jy_Zl2jp1eKttQU_gxC3nMGTChWuC8NLyncmFxoW0L1t2AVkF62JGtQ8fgnzeP5IDidclhqXafDtIkV_FG.1; fpsend=147621; __zlcmid=yzjFnky3OLinOV; SERVERID=H; ASP.NET_SessionId=pmzli2x4f0m2fw0jfdbp2aov; _gid=GA1.3.1740494310.1594452137; psortfilter=1%24all%24VOE%2FWO8MpO1adIX%2BwMGNUA%3D%3D; sidtb=Xs6HBrUnnCvh6iGaEMGmhBx2nCLrUMGh; __asc=b0a63b421733d08f828fd8fa4e2',
                'Cookie':'__asc=16dd9320173b2dbe09b0f187dc8; PRODUCT_FILTER=%7B%22TabIndex%22%3A0%2C%22SortValue%22%3A1%2C%22PageIndex%22%3A1%2C%22HashAlias%22%3A%2248f0d40b1731d909212598242194556c2306f2dde9c6827fab303276aa8fec92%22%2C%22CurrentUrl%22%3A%22https%3A//batdongsan.com.vn/nha-dat-ban%22%7D'
                # 'Upgrade-Insecure-Requests': 1
                }
from bs4 import BeautifulSoup



def get_last_page_from_bdsvn_website(url_id):
    html = request_html(url_id.url)
    soup = BeautifulSoup(html, 'html.parser')
    range_pages = soup.select('div.background-pager-right-controls > a')
    
    if range_pages:
        try:
            last_page_href =  range_pages[-1]['href']
            kq= re.search('\d+$',last_page_href)
            web_last_page_number =  int(kq.group(0))
            return web_last_page_number
        except Exception as e:
            pass
    if url_id.web_last_page_number:
        return url_id.web_last_page_number
    else:
        web_last_page_number = 1000
    return web_last_page_number

#mainfetch cho batdongsan.com.vn
class MainFetchCommonBDS(MainFetchCommon):

    def get_last_page_number(self, url_id):
        if self.fets['site_name'] =='batdongsan':
            return get_last_page_from_bdsvn_website(url_id)
        return super().get_last_page_number(url_id)
    
    def make_topic_link_from_list_id(self, list_id):
        link = super().make_topic_link_from_list_id(list_id)
        if self.fets['site_name'] =='batdongsan':
            link  = 'https://batdongsan.com.vn' +  list_id
        
        return link

    def parse_html_topic (self, topic_html):
        if self.fets['site_name'] =='batdongsan':
            topic_dict = get_bds_dict_in_topic(topic_html, self.fets['page_dict'])
            return topic_dict
        return super().parse_html_topic(topic_html)
        

    def create_page_link(self, format_page_url, page_int):
        page_url = super().create_page_link(format_page_url, page_int)
        if self.fets['site_name'] == 'batdongsan':
            page_url = format_page_url  + '/p' +str(page_int)
        return page_url

    def page_header_request(self):
        # return None
        
        if self.fets['site_name'] == 'batdongsan':
            header = {
                'Host': 'batdongsan.com.vn',
                #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                # 'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://batdongsan.com.vn/ban-nha-dat-tp-hcm/p4',
                'Connection': 'keep-alive',
                # 'Cookie':"""ASP.NET_SessionId=5nhvbogend03q5qj3vfstvng; SERVERID=B; _ga=GA1.3.1614722090.1605864505; _gid=GA1.3.5194807.1605864505; _hjid=114de2a9-a9dc-4fcc-841a-bcae203f8459; _hjIncludedInSessionSample=0; _hjAbsoluteSessionInProgress=0; __zlcmid=11GjbDIcQn8AYPg; _gcl_au=1.1.1050912898.1605864507; ins-storage-version=6; sidtb=cZqg6zF6nQYw1mqHG0IlgXga2QQ6hhsZ; usidtb=wpN0iDn5HUvuWMlHUgM2294HvYNfppJo; __cfduid=d0090b8922a57e955f2589c1e3e179e751605864583; PRODUCT_FILTER=%7B%22TabIndex%22%3A0%2C%22SortValue%22%3A1%2C%22PageIndex%22%3A1%2C%22HashAlias%22%3A%22c4bd72950aead934263568f29d2acae1cdc2fc1f0b429adc3c52a8050d2f805d%22%2C%22CurrentUrl%22%3A%22https%3A//batdongsan.com.vn/ban-nha-dat-tp-hcm%22%7D
                #    """
                # 'Cookie':"""ASP.NET_SessionId=5nhvbogend03q5qj3vfstvng; SERVERID=B; _ga=GA1.3.1614722090.1605864505; _gid=GA1.3.5194807.1605864505; _hjid=114de2a9-a9dc-4fcc-841a-bcae203f8459; __zlcmid=11GjbDIcQn8AYPg; _gcl_au=1.1.1050912898.1605864507; ins-storage-version=11; usidtb=wpN0iDn5HUvuWMlHUgM2294HvYNfppJo; __cfduid=d0090b8922a57e955f2589c1e3e179e751605864583; PRODUCT_FILTER=%7B%22TabIndex%22%3A0%2C%22SortValue%22%3A1%2C%22PageIndex%22%3A1%2C%22HashAlias%22%3A%22e17c90b5cef725e3e07b49ce83bdd862b1d7c937929e509abbfd750a18a0f8e7%22%2C%22CurrentUrl%22%3A%22https%3A//batdongsan.com.vn/ban-nha-dat%22%7D; sidtb=G7gBuCdtq7aLz3AvuursjjAPBNONVczA; _hjIncludedInSessionSample=0; _hjAbsoluteSessionInProgress=0; _gat_UA-3729099-1=1; tour-guide-ui-2020=1"""
                # 'set-cookie':"""ASP.NET_SessionId=5nhvbogend03q5qj3vfstvng; SERVERID=B; _ga=GA1.3.1614722090.1605864505; _gid=GA1.3.5194807.1605864505; _hjid=114de2a9-a9dc-4fcc-841a-bcae203f8459; _hjIncludedInSessionSample=0; _hjAbsoluteSessionInProgress=0; __zlcmid=11GjbDIcQn8AYPg; _gcl_au=1.1.1050912898.1605864507; ins-storage-version=6; sidtb=cZqg6zF6nQYw1mqHG0IlgXga2QQ6hhsZ; usidtb=wpN0iDn5HUvuWMlHUgM2294HvYNfppJo; __cfduid=d0090b8922a57e955f2589c1e3e179e751605864583; PRODUCT_FILTER=%7B%22TabIndex%22%3A0%2C%22SortValue%22%3A1%2C%22PageIndex%22%3A1%2C%22HashAlias%22%3A%22c4bd72950aead934263568f29d2acae1cdc2fc1f0b429adc3c52a8050d2f805d%22%2C%22CurrentUrl%22%3A%22https%3A//batdongsan.com.vn/ban-nha-dat-tp-hcm%22%7D
                #    """ # set-cookie không ăn sắp xếp đư

                # 'Upgrade-Insecure-Requests': 1
                }
            return header
        return super().page_header_request()
    # page handle
    def ph_parse_pre_topic(self, html_page):
        topic_data_from_pages_of_a_page = super().ph_parse_pre_topic(html_page)
        if self.fets['site_name'] == 'batdongsan':
            # self.save_to_disk(html_page, 'topic_bdscomvn_test_page_%s'%'test_page')
            # print (abc)
            soup = BeautifulSoup(html_page, 'html.parser')
            title_and_icons = soup.select('div.search-productItem')
            if title_and_icons:
                page_css_type = 1
                for title_and_icon in title_and_icons:
                    vip = title_and_icon['class'][0]
                    topic_data_from_page = {}
                    topic_data_from_page['vip'] = vip
                    title_soups = title_and_icon.select("div.p-title  a")
                    href = title_soups[0]['href']
                    topic_data_from_page['link'] = self.make_topic_link_from_list_id(href)
                    icon_soup = title_and_icon.select('img.product-avatar-img')
                    thumb = icon_soup[0]['src']
                    if 'nophoto' in thumb:
                        thumb = 'https://batdongsan.com.vn/Images/nophoto.jpg'
                    topic_data_from_page['thumb'] = thumb
                    gia_soup = title_and_icon.select('strong.product-price')
                    gia = gia_soup[0].get_text()
                    gia = gia.strip()
                    quan_huyen_str = title_and_icon.select('span.p-district strong.product-city-dist')[0].get_text()

                    topic_data_from_page['price_string'] = gia
                    quan_huyen_strs = quan_huyen_str.split(',')
                    tinh_str = quan_huyen_strs[1]
                    quan_str = quan_huyen_strs[0]
                    topic_data_from_page['region_name'] = tinh_str
                    topic_data_from_page['area_name'] = quan_str



                    date_dang = title_and_icon.select('span.uptime')
                    date_dang = date_dang[0].get_text().replace('\n','')
                    date_dang = date_dang[-10:]
                    # public_datetime = datetime.datetime.strptime(date_dang,"%d/%m/%Y")
                    # topic_data_from_page['public_datetime'] = public_datetime
                    topic_data_from_page['publish_date_str'] = date_dang
                    topic_data_from_page['thumb'] = icon_soup[0]['src']
                    topic_data_from_pages_of_a_page.append(topic_data_from_page)
            else:
                title_and_icons = soup.select('div.product-item')
                if title_and_icons:
                    page_css_type = 2
                for title_and_icon in title_and_icons:
                    vip = title_and_icon['class'][0]
                    topic_data_from_page = {}
                    topic_data_from_page['vip'] = vip
                    title_soup = title_and_icon.select(".product-title  a")[0]
                    href = title_soup['href']
                    topic_data_from_page['link'] = self.make_topic_link_from_list_id(href)

                    icon_soup = title_and_icon.select('img.product-avatar-img')[0]
                    topic_data_from_page['thumb'] = icon_soup['src']
                    gia_soup = title_and_icon.select('span.price')
                    gia = gia_soup[0].get_text()
                    gia = gia.strip()
                    quan_huyen_str = title_and_icon.select('div.product-info > span.location')[0].get_text()
                    
                    topic_data_from_page['price_string'] = gia
                    quan_huyen_strs = quan_huyen_str.split(',')
                    tinh_str = quan_huyen_strs[1]
                    quan_str = quan_huyen_strs[0]
                    topic_data_from_page['region_name'] = tinh_str
                    topic_data_from_page['area_name'] = quan_str
                  

                    date_dang = title_and_icon.select('span.tooltip-time')
                    date_dang = date_dang[0].get_text().replace('\n','')
                    public_datetime = datetime.datetime.strptime(date_dang,"%d/%m/%Y")
                    topic_data_from_page['public_datetime'] = public_datetime
                    topic_data_from_pages_of_a_page.append(topic_data_from_page)

                if not title_and_icons:
                    title_and_icons = soup.select('div.vip5')[1:]
                    if title_and_icons:
                        page_css_type = 3
                    
                    for title_and_icon in title_and_icons:
                        vip = title_and_icon['class'][0]
                        topic_data_from_page = {}
                        topic_data_from_page['vip'] = vip
                        title_soups = title_and_icon.select("div.p-title  a")
                        href = title_soups[0]['href']
                        topic_data_from_page['link'] = self.make_topic_link_from_list_id(href)
                        icon_soup = title_and_icon.select('img.product-avatar-img')
                        topic_data_from_page['thumb'] = icon_soup[0]['src']
                        gia_soup = title_and_icon.select('span.product-price')
                        gia = gia_soup[0].get_text()
                        gia = gia.strip()

                        topic_data_from_page['price_string'] = gia
                        # quan_huyen_strs = quan_huyen_str.split(',')
                        # tinh_str = quan_huyen_strs[1]
                        # quan_str = quan_huyen_strs[0]
                        # topic_data_from_page['region_name'] = tinh_str
                        # topic_data_from_page['area_name'] = quan_str

                        date_dang = title_and_icon.select('div.p-content div.mar-right-10')
                        date_dang = date_dang[0].get_text().replace('\n','')
                        date_dang = re.sub('\s*','', date_dang)
                        date_dang = date_dang[-10:]
                        public_datetime = datetime.datetime.strptime(date_dang,"%d/%m/%Y")
                        topic_data_from_page['public_datetime'] = public_datetime
                        topic_data_from_page['thumb'] = icon_soup[0]['src']
                        topic_data_from_pages_of_a_page.append(topic_data_from_page)
            # print ('***page_css_type***', page_css_type)
#             raise SaveAndRaiseException('page_bdscomvn_type_%s'%page_css_type)
            # print (aaa)
            # if topic_data_from_pages_of_a_page:
            if self.fets['is_test'] or page_css_type ==1:
                self.save_to_disk(html_page, 'bds_page_loai_%s'%page_css_type)
        return topic_data_from_pages_of_a_page





def get_phuong_xa_from_topic(self,soup):
    sl = soup.select('div#divWard li.current')   
    if sl:
        phuong_name =  sl[0].get_text()
    else:
        phuong_name =  False
    return phuong_name


def get_images_for_bds_com_vn(soup):
    rs = soup.select('meta[property="og:image"]')
    images =  list(map(lambda i:i['content'], rs))
    return images


def get_public_datetime(soup):
    try:
        select = soup.select('div.prd-more-info > div:nth-of-type(3)')#[0].contents[0]
        publish_date_str = select[0].contents[2]
    except IndexError:
        pass
    publish_date_str = publish_date_str.replace('\r','').replace('\n','')
    publish_date_str = re.sub('\s*', '', publish_date_str)
    public_datetime = datetime.datetime.strptime(publish_date_str,"%d-%m-%Y")
    return public_datetime


def get_product_detail(soup, type_bdscom_topic = 1):
    if type_bdscom_topic==1:
        select = soup.select('div.pm-desc')[0]
    elif type_bdscom_topic==2:
        
        select = soup.select('div.des-product')[0]
        
    return select.get_text()
    

def get_mobile_name_for_batdongsan(soup):
    phone = get_mobile_user(soup)
    try:
        name = get_user_name(soup)
    except:
        name = 'no name bds'
    return phone, name
   

def get_dientich(soup):
    try:
        kqs = soup.find_all("span", class_="gia-title")
        gia = kqs[1].find_all("strong")
    except:
        try:
            gia = soup.select('div.short-detail-wrap > ul.short-detail-2 > li:nth-of-type(2) > span.sp2')
        except:
            raise 
    try:
        gia = gia[0].get_text()
    except:
        return False
    try:
        rs = re.search(r"(\d+)", gia)
        gia = rs.group(1)
    except:
        gia = 0
    float_gia = float(gia)
    return float_gia


def get_mobile_user(soup):
    # mobile = False
    try:
        select = soup.select('div#LeftMainContent__productDetail_contactMobile')[0]
        mobile =  select.contents[3].contents[0]
        mobile =  mobile.strip()
        # raise SaveAndPass('bds_mobile_loai_1')
        # return mobile
    except IndexError:
        try:
            select = soup.select('span.phoneEvent')[0]
            phone = select['raw']
            # raise SaveAndPass('bds_mobile_loai_2')
        except IndexError:
            select = soup.select('#divCustomerInfoAd div.right-content .right')[0]
            phone = select.get_text()
            # raise SaveAndPass('bds_mobile_loai_3')
        mobile = phone
    if not mobile:
        raise ValueError('not phone')
    return mobile
    

def get_user_name(soup):
    name = False
    try:
        select = soup.select('div#LeftMainContent__productDetail_contactName')[0]
        name =  select.contents[3].contents[0]
        name =  name.strip()

    except:
        select = soup.select('dive.name')[0]
        name = select['title']
   
    if not name:
        raise ValueError('name')
    return name

    
# tại sao lại nằm ở đây
def get_bds_dict_in_topic( topic_html, page_dict):
    update_dict = {}
#     update_dict['data'] = html
    soup = BeautifulSoup(topic_html, 'html.parser')
    # self.save_to_disk(html_page, 'topic_bdscomvn_page_loai_%s'%'test')
    # print (abc)
    try:
        kqs = soup.find_all("span", class_="gia-title")
        gia = kqs[0].find_all("strong")
        gia = gia[0].get_text()
        type_bdscom_topic = 1
        self.save_to_disk(html_page, 'topic_bdscomvn_page_loai_%s'%type_bdscom_topic)
    except:
        gia_soup = soup.select("div.short-detail-wrap > ul.short-detail-2 > li:nth-of-type(1) > span.sp2")[0]
        gia = gia_soup.get_text()
        type_bdscom_topic = 2
    update_dict['price_string'] = gia

    if type_bdscom_topic == 2:
        gia_soup = soup.select("div.product-config ul.short-detail-2 li:nth-of-type(1) span:nth-of-type(2)")[0]
        gia = gia_soup.get_text()
        update_dict['publish_date_str'] = gia

        gia_soups = soup.select("div.breadcrumb > a")

        region_name = gia_soups[1].get_text()
        update_dict['region_name'] = region_name

        area_name = gia_soups[2].get_text()
        update_dict['area_name'] = area_name

    
    
    update_dict['html'] = get_product_detail(soup, type_bdscom_topic)
    images = get_images_for_bds_com_vn(soup)
    if images:
        update_dict['images'] = images
    update_dict['area'] = get_dientich(soup)
    try:
        title = soup.select('div.pm-title > h1')[0].contents[0] 
    except:
        try:
            title = soup.select('h1.tile-product')[0].get_text()
        except:
            raise 
    update_dict['title']=title
    update_dict['phone'], update_dict['account_name'] = get_mobile_name_for_batdongsan(soup)
    try:
        loai_nha = soup.select('span.diadiem-title a')[0].get_text()
        loai_nha_search = re.search('(^.*?) tại', loai_nha)
        loai_nha = loai_nha_search.group(1)
    except:
        try:
            loai_nha = soup.select('div.breadcrumb a')[-1].get_text()
            loai_nha_search = re.search('(^.*?) tại', loai_nha)
            loai_nha = loai_nha_search.group(1)
        except:
            loai_nha = soup.select('span.diadiem > strong')[0].get_text()
    loai_nha = re.sub('^bán |^cho thuê ','',loai_nha, flags=re.I)  
    loai_nha = loai_nha.capitalize()    
    update_dict['loai_nha'] = loai_nha  

    for key, value in update_dict.items():
        if key not in page_dict:
            page_dict[key]  = value
    return page_dict

# gán lại  1
MainFetchCommon = MainFetchCommonBDS

################## mua ban ############################
class MuabanFetch(MainFetchCommon):
    # _inherit = 'abstract.main.fetch'

    def get_last_page_number(self, url_id):
        if self.fets['site_name'] =='muaban':
            return 300
        return super(MuabanFetch, self).get_last_page_number(url_id)
        
    def parse_html_topic (self, topic_html):
        if self.fets['site_name'] =='muaban':
            topic_dict = MuabanObject().get_topic(topic_html)
            return topic_dict
        return super(MuabanFetch, self).parse_html_topic(topic_html)

    def create_page_link(self, format_page_url, page_int):
        page_url = super(MuabanFetch, self).create_page_link(format_page_url, page_int)
        repl = '?cp=%s'%page_int
        if self.fets['site_name'] == 'muaban':
            if 'cp=' in format_page_url:
                page_url =  re.sub('\?cp=(\d*)', repl, format_page_url)
            else:
                page_url = format_page_url +  '?' + repl
        return page_url

    def ph_parse_pre_topic(self, html_page):
        topic_data_from_pages_of_a_page = super(MuabanFetch, self).ph_parse_pre_topic(html_page)
        if self.fets['site_name'] == 'muaban':
            a_page_html_soup = BeautifulSoup(html_page, 'html.parser')
            title_and_icons = a_page_html_soup.select('div.list-item-container')
            for title_and_icon in title_and_icons:
                topic_data_from_page = {}
                image_soups = title_and_icon.select("a.list-item__link")
                image_soups = image_soups[0]
                href = image_soups['href']
                img = image_soups.select('img')[0]
                src_img = img.get('data-src',False)
                topic_data_from_page['link'] = self.make_topic_link_from_list_id(href)
                topic_data_from_page['thumb'] = src_img
                area = 0
                try:
                    area = title_and_icon.select('span.list-item__area b')[0].get_text()
                    area = area.split(' ')[0].strip().replace(',','.')
                    try:
                        area = float(area)
                    except:
                        area = 0
                except IndexError:
                    pass
                topic_data_from_page['area']=area
                
                gia_soup = title_and_icon.select('span.list-item__price')
                if gia_soup:
                    gia = gia_soup[0].get_text()
                else:
                    gia = False
                
                topic_data_from_page['price_string'] = gia
                ngay_soup = title_and_icon.select('span.list-item__date')
                ngay = ngay_soup[0].get_text().strip().replace('\n','')
                public_datetime = datetime.datetime.strptime(ngay,"%d/%m/%Y")
                topic_data_from_page['public_datetime'] = public_datetime  
                topic_data_from_pages_of_a_page.append(topic_data_from_page)
        return topic_data_from_pages_of_a_page

# gán lại 2
MainFetchCommon = MuabanFetch


class MuabanObject():
    def write_images(self, soup):
        update_dict = {}
        image_soup = soup.select('div.image__slides img')
        images = [i['src'] for i in image_soup]
        update_dict['images'] = images
        return update_dict

    def write_gia_tho(self, soup):
        gia_soup = soup.select('div.price-container__value')
        try:
            gia =  gia_soup[0].get_text()
        except IndexError:
            gia = False
        return {'price_string':gia}
    # dữ liệu thô
    def write_quan_phuong_tho(self, soup):
        quan_soup = soup.select('span.location-clock__location')
        quan_txt =  quan_soup[0].get_text()
        quan_tinhs = quan_txt.split('-')
        tinh_name = quan_tinhs[1].strip()
        tinh_name = re.sub('tphcm','Hồ Chí Minh', tinh_name,flags=re.I)
        quan_name =  quan_tinhs[0].strip()
        return {'region_name':tinh_name, 'area_name':quan_name}

    def write_poster_tho(self, soup):
        try:
            name_soup = soup.select('div.user-info__fullname')[0]
            name =  name_soup.get_text()
        except:
            name = None
        try:
            span_mobile_soup = soup.select('div.mobile-container__value span')[0]
            mobile = span_mobile_soup['mobile']
        except:
            mobile = None
        mobile = mobile or 'No Mobile'
        name = name or mobile
        return {'phone':mobile, 'account_name':name}

    def get_loai_nha(self, soup):
        loai_nha_soup = soup.select('div.breadcrumb li')
        loai_nha = loai_nha_soup[-1].get_text()
        return {'loai_nha':loai_nha}

    def get_topic(self, html):
        update_dict  = {}
        soup = BeautifulSoup(html, 'html.parser')
        content_soup = soup.select('div.body-container')
        update_dict['html']  = content_soup[0].get_text()
        update_dict.update(self.write_gia_tho(soup))
        update_dict.update(self.write_quan_phuong_tho(soup))
        update_dict.update(self.get_loai_nha(soup))
        update_dict.update(self.write_poster_tho(soup))
        title = soup.select('h1.title')[0].get_text()
        title = title.strip()
        update_dict['title'] = title
        return update_dict
################## !mua ban ###########################

############ Tạp hóa ############################

class TapHoaMainFetch(MainFetchCommon):

    def get_main_obj(self):
        rs = super().get_main_obj()
        if self.fets['site_name'] =='cuahangtaphoa' or self.fets['model_name']=='tap.hoa':
            return self.env['tap.hoa']
        return rs

    def get_last_page_number(self, url_id):
        if self.fets['site_name'] =='cuahangtaphoa':
            if url_id.web_last_page_number:
                return url_id.web_last_page_number
            return 300
        return super().get_last_page_number(url_id)

    def get_dia_chi(self, topic_soups, dia_chi_str= 'Địa chỉ:'):
        try:
            ngay_cap_soup = topic_soups.select("li:contains('%s')"%dia_chi_str)[0]
            ngay_cap = ngay_cap_soup.get_text().split(':')[1].strip()
        except IndexError:
            ngay_cap = None
        return ngay_cap

    def parse_html_topic (self, topic_html):
        
        if self.fets['site_name'] =='cuahangtaphoa' or self.fets['model_name']=='tap.hoa':
            topic_dict = {}
            a_page_html_soup = BeautifulSoup(topic_html, 'html.parser')
            topic_soups = a_page_html_soup.select('div.item-page')[0]
            try:
                nghanh_nghe_soup = topic_soups.select("li:contains('Ngành nghề chính: ')")[0]
                nghanh_nghe = nghanh_nghe_soup.get_text().split(':')[1]
                nghanh_nghe = nghanh_nghe.replace('./.','').strip()
            except IndexError:
                nghanh_nghe = False

            topic_dict['nganh_nghe_kinh_doanh'] = nghanh_nghe

            return topic_dict
        return super().parse_html_topic(topic_html)

    def create_page_link(self, format_page_url, page_int):
        page_url = super().create_page_link(format_page_url, page_int)
        if self.fets['site_name'] == 'cuahangtaphoa':
            repl = 'page-%s'%page_int
            page_url =  re.sub('page-\d+', repl, format_page_url)
        return page_url

    def request_and_parse_html_topic(self, link):
        topic_dict = super().request_and_parse_html_topic(link)
        if self.fets['site_name'] =='cuahangtaphoa' or self.fets['model_name'] =='tap.hoa':
            topic_dict['is_full_topic'] = True
        return topic_dict

    def get_st_is_bds_site(self):
        if self.fets['site_name'] =='cuahangtaphoa' or self.fets['model_name'] =='tap.hoa':
            return False
        return super().get_st_is_bds_site()
    
    def ph_parse_pre_topic(self,html_page):
        topic_data_from_pages_of_a_page = super().ph_parse_pre_topic(html_page)
        if self.fets['site_name'] == 'cuahangtaphoa':
            a_page_html_soup = BeautifulSoup(html_page, 'html.parser')
            title_and_icons = a_page_html_soup.select('div.news-v3')
            if not title_and_icons:
                raise UserError('Không có topic nào từ page của muaban')
            for title_and_icon in title_and_icons:
                topic_data_from_page = {}
                try:
                    chu_so_huu_soup = title_and_icon.select('a')[0]
                    chu_so_huu = chu_so_huu_soup.get_text()
                    topic_data_from_page['name_of_poster'] = chu_so_huu
                    mst_tag = title_and_icon.select('a')[1]
                    href = mst_tag['href']
                    title = mst_tag['title']
                    mst = mst_tag.get_text()
                    phone = re.search(' (\d{7,})$', title)
                    if phone:
                        phone = phone.group(1)
                        topic_data_from_page['poster_id'] = phone
                    else:
                        phone = False
                except IndexError:
                    href = 'n/a'
                    title = False
                dia_chi_soup = title_and_icon.select("p:contains('Địa chỉ:')")[0]
                dia_chi = dia_chi_soup.get_text()
                dia_chis = dia_chi.split(',')  
                tinh = dia_chis[-1]
                quan = dia_chis[-2]
                try:
                    phuong = dia_chis[-3]
                except:
                    phuong = False

                try:
                    duong = dia_chis[-4]
                    duong = duong.replace('Địa chỉ: ')
                except:
                    duong = False
                ngay_thanh_lap_soup = title_and_icon.select("p:contains('Ngày thành lập: ')")[0]
                ngay_thanh_lap = ngay_thanh_lap_soup.get_text()
                ngay_thanh_lap_search = re.search('Ngày thành lập: ([\d/]+) \(', ngay_thanh_lap)
                if ngay_thanh_lap_search:
                    ngay_thanh_lap = ngay_thanh_lap_search.group(1)
                    format_str = '%d/%m/%Y' # The format
                    public_date = datetime.datetime.strptime(ngay_thanh_lap, format_str).date()
                    
                else:
                    ngay_thanh_lap = False
                    public_date = False
                topic_data_from_page['public_date'] = public_date
                topic_data_from_page['ngay_thanh_lap'] = ngay_thanh_lap
                topic_data_from_page['tinh']=tinh
                topic_data_from_page['quan']=quan
                topic_data_from_page['phuong']=phuong
                topic_data_from_page['duong']=duong
                topic_data_from_page['link'] = href
                topic_data_from_page['mst'] = mst
                topic_data_from_page['address'] = dia_chi
                topic_data_from_page['title'] = title
                topic_data_from_page['html'] = ''
                topic_data_from_pages_of_a_page.append(topic_data_from_page)
        return topic_data_from_pages_of_a_page



class BDSProject(MainFetchCommon):


    def get_main_obj(self):
        rs = super().get_main_obj()
        if self.fets['site_name'] =='chotot_duan':
            return self.env['bds.project']
        return rs


    def get_search_domain(self, link, topic_data_from_page):
        if self.fets['site_name'] =='chotot_duan':
            return [('name', '=', topic_data_from_page['name'])]
        return super().get_search_domain(link, topic_data_from_page)


    def get_last_page_number(self, url_id):
        return 400

    # def parse_html_topic (self, topic_html):
        
    #     if self.fets['site_name'] =='cuahangtaphoa' or self.fets['model_name']=='tap.hoa':
    #         topic_dict = {}
    #         a_page_html_soup = BeautifulSoup(topic_html, 'html.parser')
    #         topic_soups = a_page_html_soup.select('div.item-page')[0]
    #         try:
    #             nghanh_nghe_soup = topic_soups.select("li:contains('Ngành nghề chính: ')")[0]
    #             nghanh_nghe = nghanh_nghe_soup.get_text().split(':')[1]
    #             nghanh_nghe = nghanh_nghe.replace('./.','').strip()
    #         except IndexError:
    #             nghanh_nghe = False

    #         topic_dict['nganh_nghe_kinh_doanh'] = nghanh_nghe

    #         return topic_dict
    #     return super().parse_html_topic(topic_html)

    def create_page_link(self, format_page_url, page_int):
        page_url = super().create_page_link(format_page_url, page_int)
        if self.fets['site_name'] == 'chotot_duan':
            if page_int > 0:
                offset = (page_int - 1)*10
            else:
                offset = 0
            repl = 'offset=%s'%offset
            page_url =  re.sub('offset=10', repl, format_page_url)
        return page_url


    def get_st_is_bds_site(self):
        if self.fets['site_name'] =='chotot_duan':
            return False
        return super().get_st_is_bds_site()
    
    def ph_parse_pre_topic(self,html_page):
        topic_data_from_pages_of_a_page = super().ph_parse_pre_topic(html_page)
        if self.fets['site_name'] == 'chotot_duan':
            topic_data_from_pages_of_a_page = []
            json_a_page = json.loads(html_page)
            topic_data_from_pages_of_a_page_origin = json_a_page['projects']
            for ad in topic_data_from_pages_of_a_page_origin:
                topic_data_from_page = {}
                # topic_data_from_page['price_string'] = ad['price_string']
                # topic_data_from_page['price'] = ad['price']
                # topic_data_from_page['gia'] = ad['price']/1000000000
                # topic_data_from_page['date'] = ad['date']
                # topic_data_from_page['link'] = None
                # topic_data_from_page['html'] = ad['body']
                topic_data_from_page['name']= ad['project_name']
                print ('11'*30, ad['project_name'])
                # topic_data_from_page['region_name'] = ad['region_name']
                # topic_data_from_page['area_name'] = ad['area_name']
                # try:
                #     topic_data_from_page['ward_name'] = ad['ward_name']
                # except:
                #     pass
                
                # if 'image' in ad:
                #     topic_data_from_page['thumb'] = ad['image']
                # if 'company_ad' in ad:
                #     company_ad = ad['company_ad']
                # else:
                #     company_ad = False 
                # topic_data_from_page['chotot_moi_gioi_hay_chinh_chu'] = \
                # 'moi_gioi' if company_ad else 'chinh_chu' 
                # if 'category_name' in ad:
                #     category_name = ad['category_name']
                #     topic_data_from_page['loai_nha'] =  category_name
                # else:
                #     topic_data_from_page['loai_nha'] =  False
                topic_data_from_pages_of_a_page.append(topic_data_from_page)
        return topic_data_from_pages_of_a_page





# gán lại 3
MainFetchCommon = TapHoaMainFetch


#chotot_duan

# class ChoTotDuan(MainFetchCommon):

#     def get_main_obj(self):
#         rs = super().get_main_obj()
#         if self.fets['site_name'] =='chotot_duan':
#             return self.env['bds.project']
#         return rs
##################! tạp hóa#######
############# COMPUTE FUNCTION ###############


def _compute_so_phong_ngu( html):
        so_phong_ngu = 0
        pt = '(\d{1,2})\s*(?:pn|phòng ngủ)(?:\W|$)'
        rs = re.search(pt, html, re.I)
        if rs:
            so_phong_ngu = rs.group(1)
            try:
                so_phong_ngu = int(so_phong_ngu)
            except: 
                so_phong_ngu = 0
        return so_phong_ngu

def detect_mat_tien_address(html, p = None):
    #parent function call: detect_mat_tien_address_sum
    before_index = 0
    deal_s = []
    full_adress_list = []
    while 1:
        html = html [before_index:]
        # p = '(?i:nhà|mt|mặt tiền|số)\s+(\d{1,4}[a-zA-Z]{0,2})[\s,]+(?i:đường)*\s*(?P<ten_duong>(?:[A-Z0-9Đ][\w|/]*\s*){1,4})(?:\.|\s|\,|$|<)'
        mat_tien_full_address_possibles = re.search(p, html, re.I)  #((\S+(?:\s|\.|$|,)+){1,4})
        if not mat_tien_full_address_possibles:
            break
        if mat_tien_full_address_possibles:
            before_index = mat_tien_full_address_possibles.span()[1] + 1
            number = mat_tien_full_address_possibles.group(1)
            ten_duong = mat_tien_full_address_possibles.group('ten_duong')
            is_check_word = re.search('[a-zđ]',ten_duong, re.I)
            if not is_check_word:
                continue
            full_address = number + ' ' +  ten_duong
            full_address_unidecode = unidecode(full_address)
            if number not in deal_s:
                deal_s.append(number)
                sxs = re.search('x(?: |$)|^[x\d\s]+$',ten_duong, re.I) # có x trong tên đường
                if sxs:
                    continue
                ddm = re.search('(?:^|x|\*|\s)\s*\d+m',full_address, re.I)# check mét
                if ddm:
                    continue

                check_co_word = re.search('\D', full_address)
                if not check_co_word:
                    continue
                ten_duong_lower = ten_duong.strip().lower() 
                if ten_duong_lower in ['căn']:
                    continue
                pt = 'MT|Lầu|tỷ|căn|phòng|tấm|PN|WC|mặt|trệt|tầng|sẹc|sẹt|xẹc|xẹt|lửng|lững|trục đường|\dt\s*\dl'
                pt = unidecode(pt)
                is_mt = re.search(pt, full_address_unidecode, re.I)
                if is_mt:
                    continue
                bao_nhieu_met = re.search('\d+m|\dT', number, re.I)
                if bao_nhieu_met:
                    continue
                co_format_sdt = re.search('[\d\s]{6,}|3 Tháng 2|đi |thẳng |\d+(?:tr|t) \dL', full_address)
                if co_format_sdt:
                    continue
                if len(ten_duong) == 1:
                    continue
                index = mat_tien_full_address_possibles.span()[0]
                pre_index = index - 12
                if pre_index < 0:
                    pre_index = 0
                check_hem_string = html[pre_index:index]
                if check_hem_string:
                    is_hem = re.search('hẻm|hxt|đường|bđs|cty|nhà đất|vp|văn phòng|phường|quận', check_hem_string, re.I)
                    if is_hem:
                        continue
                full_adress_list.append((number, full_address))
    return full_adress_list

def detect_mat_tien_address_sum(html):
    #parent function call: _compute_mat_tien_or_trich_dia_chi
    full_adress_list_sum =  []
    number_list_sum = []
    addresses = {
    'html':{'value':html,
        'p':'(?<!cách )(?i:nhà|mt|mặt tiền|số)\s+(\d{1,4}[a-zA-Z]{0,2})[\s,]+(?i:đường)*\s*(?P<ten_duong>(?-i:[A-Z0-9Đ][\w|/]*\s*){1,4})(?:\.|\s|\,|$|<)'
        }, 
    }
    for key,val in addresses.items():
        html = val['value']
        p = val['p']
        if html:
            mat_tien_adress_list = detect_mat_tien_address(html, p)
            if mat_tien_adress_list:
                for number, full_address in mat_tien_adress_list:
                    if number not in number_list_sum:
                        full_adress_list_sum.append(full_address)
                        number_list_sum.append(number)
    mat_tien_address = False                  
    if full_adress_list_sum:
        mat_tien_address = ','.join(full_adress_list_sum)
    return mat_tien_address

def trim_street_name(street_name_may_be):
    #pr: detect_trich_dia_chi
    rs = re.sub(',|\.','', street_name_may_be, flags=re.I)
    rs = rs.strip()
    return rs

def detect_trich_dia_chi(address):
    if not address:
        return 
    #@pr: detect_trich_dia_chi_list
    keys_street_has_numbers = ['3/2','30/4','19/5','3/2.','3/2,','23/9']
    pat_247 = '24h*/7|24h*/24|1/500'
    hem_full_addresses = []
    hem_address_numbers = []
    index_before = 0
    while 1:
        address = address[index_before:]
        posible_address_search = re.search('(?P<adress_number>\d+\w{0,2}/\d+\w{0,2}(?:/\d+\w{0,2})*)[\s,]+(?:đường[\s,]+)*(?P<ten_duong>(?:[\w|/]+\s*){1,4})(?:\.|\s|,|$)', address)
        if posible_address_search:
            index_before = posible_address_search.span()[1]
            adress_number = posible_address_search.group('adress_number')
            street_name = posible_address_search.group('ten_duong')
            street_name = trim_street_name(street_name)
            full_adress = adress_number +' ' + street_name
            if adress_number not in hem_address_numbers:
                black_list = '23/23 Nguyễn Hữu Tiến|5 Độc Lập'
                black_list_rs = re.search(black_list, address, re.I)
                if black_list_rs:
                    hem_address_numbers.append(adress_number)
                    continue
                rs = re.search('\d+m',street_name, re.I)
                if  rs:
                    continue
                if adress_number in ['1/2','50/100','100/100']:
                    continue
                rs = re.search(pat_247, adress_number, re.I)
                if rs:
                    continue
                if adress_number in keys_street_has_numbers:
                    # street_result_keys.append(adress_number)
                    continue
                is_day = re.search('\d+/\d\d\d\d', adress_number)
                if is_day:
                    continue
                pnwc = re.search('(?:pn|wc|x|50/50)', adress_number, re.I)
                if pnwc:
                    continue
                is_ty_m2 =  re.search('tỷ|tr|m2', full_adress, re.I)
                if is_ty_m2:
                    continue
                index = posible_address_search.span()[0]
                before_index = index -20
                if before_index < 0:
                    before_index = 0
                before_string = address[before_index: index]
                is_van_phong = re.search('văn phòng|vp|bđs|nhà đất|[\d]{4,}', before_string, re.I)
                if is_van_phong:
                    continue
                before_index = index -5
                if before_index < 0:
                    before_index = 0
                before_string = address[before_index: index]
                is_van_phong = re.search('hẻm|hẽm', before_string, re.I)
                if is_van_phong:
                    continue
                hem_full_addresses.append((adress_number, full_adress))
                hem_address_numbers.append(adress_number)
        else:
            break
    return hem_full_addresses

def detect_trich_dia_chi_list(address_list):
    if not address_list:
        return 
    #pr: _compute_mat_tien_or_trich_dia_chi
    sum_full_hem_address = [] 
    only_number_address_sum_full_hem_address = [] 
    for ad in address_list:
        hem_full_addresses = detect_trich_dia_chi(ad)
        if not hem_full_addresses:
            return 
        for i in hem_full_addresses:
            number_address = i[0]
            if number_address not in only_number_address_sum_full_hem_address:
                sum_full_hem_address.append(i)
                only_number_address_sum_full_hem_address.append(number_address)
    return sum_full_hem_address

def _compute_mat_tien_or_trich_dia_chi(self, html, html_trich_dia_chi, r):#compute
        mat_tien_address = detect_mat_tien_address_sum(html)
        trich_dia_chi = False
        address_list = [html_trich_dia_chi]
        sum_full_hem_address = detect_trich_dia_chi_list(address_list)
        if sum_full_hem_address:
            trich_dia_chi = ','.join(map(lambda i:i[1], sum_full_hem_address))
        mat_tien_or_trich_dia_chi = mat_tien_address or trich_dia_chi
        is_mat_tien_or_trich_dia_chi ='1' if  bool(mat_tien_or_trich_dia_chi) else '0'
        
        if trich_dia_chi:
            same_address_bds_ids  = self.env['bds.bds'].search([('trich_dia_chi','=ilike',trich_dia_chi),('id','!=',r.id)])
            same_address_bds_ids = [(6,0,same_address_bds_ids.mapped('id'))]
        else:
            same_address_bds_ids = False
        return mat_tien_address, trich_dia_chi, mat_tien_or_trich_dia_chi, is_mat_tien_or_trich_dia_chi, same_address_bds_ids

def _compute_mat_tien_or_trich_dia_chi1(self, html, html_trich_dia_chi):#compute
    mat_tien_address = detect_mat_tien_address_sum(html)
    trich_dia_chi = False
    address_list = [html_trich_dia_chi]
    sum_full_hem_address = detect_trich_dia_chi_list(address_list)
    mat_tien_or_trich_dia_chis = []
    if mat_tien_address:
        mat_tien_or_trich_dia_chis.append(mat_tien_address)
    if sum_full_hem_address:
        for i in sum_full_hem_address:
            mat_tien_or_trich_dia_chis.append(i[1])
    if mat_tien_or_trich_dia_chis:
        mat_tien_or_trich_dia_chi = ','.join(mat_tien_or_trich_dia_chis)
    else:
        mat_tien_or_trich_dia_chi = False

    # mat_tien_or_trich_dia_chi = mat_tien_address or trich_dia_chi
    is_mat_tien_or_trich_dia_chi ='1' if  bool(mat_tien_or_trich_dia_chi) else '0'
    return mat_tien_address, trich_dia_chi, mat_tien_or_trich_dia_chi, is_mat_tien_or_trich_dia_chi


def compute_t1l1_detect(html):
    #@pr: _compute_kw_mg
    t1l1_list = []
    pt = '(1t[,\s]*(\d{1,2})l)(?:\W|$)'
    rs = re.search(pt, html, re.I)
    if rs:
        t1l1_list.append(rs.group(1))
    pt = '((\d{1,2})\s*pn)(?:\W|$)'
    rs = re.search(pt, html, re.I)
    if rs:
        t1l1_list.append(rs.group(1))
    pt = '(?:\W|^)(st)(?:\W|$)'
    rs = re.search(pt, html, re.I)
    if rs:
        t1l1_list.append(rs.group(1))
        
    return t1l1_list


def _compute_kw_mg( html):
        if not html:
            return 
        found_kw_mgs = []
        pat_247 = '24h*/7|(?<!an ninh )24h*/24|1/500'
        rs = re.search(pat_247, html, re.I)
        kw_co_date = False #1
        if rs:
            found_kw_mgs.append(rs.group(0))
            kw_co_date = rs.group(0)
        nha_dat_kws_cap_1 = 'nhà đất(?! thánh)|uy tín|real|bds|bđs|cần tuyển|tuyển sale|tuyển dụng|bất động sản|bđs|ký gửi|kí gửi|'+\
        '(?<!nova)land(?!mark|abc)|tư vấn|(?:thông tin|sản phẩm) (?:chính xác|thật)|' +\
        'xem nhà miễn phí|(?:hổ|hỗ) trợ miễn phí|khách hàng|' +\
        'hỗ trợ[\w\s]{0,20}pháp lý|hợp.{1,20}đầu tư|csht|tttm|'+\
        'chưa qua đầu tư|cấp 1[,\- ]*2[,\- ]*3|'+\
        'tiện kinh doanh[ ,]{1,2}buôn bán[ ,]{1,2}mở công ty[ ,]{1,2}văn phòng|nợ ngân hàng|hợp tác|thanh lý' 

     
        nha_dat_list_rs = re.findall(nha_dat_kws_cap_1, html, re.I)
        if nha_dat_list_rs:
            found_kw_mgs.extend(nha_dat_list_rs)

        mtg_kws = 'mmg|mqc|mtg|(?-i:MTKD)|(?-i:BTCT)|(?-i:CHDV)|(?-i:DTSD)|(?:.{0,10}cho khách?:.{0,10})|(?:khu vực an ninh|dân trí cao)\W{1,3}(?:khu vực an ninh|dân trí cao)'
        nha_dat_list_rs = re.findall(mtg_kws, html, re.I)
        kw_mg_cap_2 = False #2
        is_kw_mg_cap_2 = False#3
        if nha_dat_list_rs:
            kw_mg_cap_2 = ','.join(nha_dat_list_rs)
            is_kw_mg_cap_2 = True

        break_kw = '(\n✓|\n\*)'
        break_rs = re.findall(break_kw, html, re.I)
        kw_co_special_break = False # 4
        if break_rs:
            len_break_rs = len(break_rs)
            kw_co_special_break = len_break_rs
       
        break_kw = '(\n)'
        break_rs = re.findall(break_kw, html, re.I)
        kw_co_break = False # 5
        if break_rs:
            len_break_rs = len(break_rs)
            kw_co_break = len_break_rs
        number_char = len(html)
        hoa_la_canh_pt = '🏠|💥|✅|👉🏻|⭐️|💵|💰|☎️|⚡|📲|💎|🌹|☎|🌈|🍎|🍏|🏦|📣|🆘|☎️|🤝|👍|👉|' +\
            '🏡|🗽|🎠|🏖|😍|🔥'
        nha_dat_list_rs = re.findall(hoa_la_canh_pt, html, re.I)
        hoa_la_canh = False # 6
        if nha_dat_list_rs:
            hoa_la_canh = len(nha_dat_list_rs)
        t1l1_list = compute_t1l1_detect(html)
        t1l1 = False #7
        if t1l1_list:
            t1l1 = ','.join(t1l1_list)
        kw_mg = False #8
        dd_tin_cua_co = 'no_kw_co_cap_1' # 9
        if found_kw_mgs:
            kw_mg = ','.join(found_kw_mgs)
            dd_tin_cua_co = 'kw_co_cap_1'

        return kw_co_date, kw_mg_cap_2, is_kw_mg_cap_2, kw_co_special_break, kw_co_break,\
                hoa_la_canh, t1l1, kw_mg, dd_tin_cua_co

def str_before_index(index, input_str):
    #@pr: _compute_dd_tin_cua_dau_tu
    pre_index = index - 30
    if pre_index < 0:
        pre_index = 0
    pre_str = input_str[pre_index:index]
    return pre_str

def _compute_dd_tin_cua_dau_tu(html):
        p = '((?<=\W)(?:hoa hồng|hh(?!t)|huê hồng|🌹)\s*(?:cho)*\s*(?:mg|môi giới|mô giới|TG|Trung gian)*\s*(?:\D|\s){0,31}((\d|\.)+\s*(%|triệu|tr))*)(?:\s+|$|<|\.|)'
        rs = re.search(p, html, re.I)
        if not rs:
            p = '((?:phí(?! hh| hoa hồng| huê hồng|\w)|chấp nhận)\s*(?:cho)*\s*(?:mg|môi giới|mô giới|TG|Trung gian)*\s*((\d|\.)+\s*(%|triệu|tr))*)(?:\s+|$|<|\.|)'
            rs = re.search(p, html, re.I)
        kw_hoa_hong, kw_so_tien_hoa_hong, dd_tin_cua_dau_tu = False, False, False
        if rs:
            for i in [1]:
                index = rs.span()[0]
                pre_str = str_before_index(index, html)
                khong_cho_mg = re.search('không|ko', pre_str, re.I)
                if khong_cho_mg:
                    continue
                kw_hoa_hong_tach = rs.group(1)
                kw_hoa_hong_tach = kw_hoa_hong_tach.strip().lower()
                if kw_hoa_hong_tach in  ['phí', 'chấp nhận']:
                    continue
                kw_hoa_hong = kw_hoa_hong_tach
                kw_so_tien_hoa_hong = rs.group(2)
                dd_tin_cua_dau_tu = True
        else:
            rs = re.search('((1)%)', html, re.I)
            if rs:
                kw_hoa_hong = rs.group(1)
                kw_so_tien_hoa_hong = rs.group(2)
                dd_tin_cua_dau_tu = True
        return kw_hoa_hong, kw_so_tien_hoa_hong, dd_tin_cua_dau_tu


def detect_is_mat_tien(html):
    if not html:
        return 
    #@pr: _compute_loai_hem_combine
    while 1:
        p = '(?:(?<!2 )mặt tiền|nhà mt|mặt phố)(?! hẻm)'
        rs = re.search(p, html, re.I)
        hxh_str, full_hxh,is_mat_tien = False,False,False
        if rs:
            span0 = rs.span(0)[0]
            pre_index = span0-10
            if pre_index<0:
                pre_index = 0
            pre = html[pre_index:span0]
            gan_sat_cach_pt = 'gần|sát|cách|hai|từ|ra|sau lưng|hai'
            gan_sat_cach_search = re.search(gan_sat_cach_pt,pre, re.I)
            if gan_sat_cach_search:
                before_index = rs.span()[1] + 1
                html = html[before_index:]
                continue
            hxh_str = rs.group(0)
            full_before_index = rs.span(0)[1] + 10
            full_hxh = html[pre_index:full_before_index]
            is_mat_tien = True
            return hxh_str, full_hxh, is_mat_tien
        else:
            return hxh_str, full_hxh, is_mat_tien        


def cach_search(pre):
    #pr: detect_hem_rong()
    gan_sat_cach_pt = 'cách'
    gpxd_search = re.search(gan_sat_cach_pt,pre, re.I)
    return gpxd_search

def previous_of_match(html, rs_group, previous_char_number = 30):
    #pr: detect_hem_rong()
    span0 = rs_group.span(0)[0]
    pre_index = span0-previous_char_number
    pre = html[pre_index:span0]
    return pre
    
def detect_hem_rong(html):
    #@pr: _compute_loai_hem_combine
    while 1:
        pt = '(?<!cách )(?:hẻm|hẽm|đường)\s+(?:trước nhà)*\s*(?:xh|xe hơi|ô tô|xe máy|kia|ba gác|ba gát)*\s*(?:trước nhà)*\s*(?:nhỏ)*\s*(?:rộng)*\s*(?:khoảng|tầm)*\s*(\d+(?:\.|m|mét|,)*\d*)\s*(?:m|mét)*(?:\W|$)'
        rs = re.search(pt, html, re.I)
        if rs:
            pre = previous_of_match(html, rs)
            cach_search_rs = cach_search(pre)
            if cach_search_rs:
                before_index = rs.span(0)[1] + 1
                html = html[before_index:]
                continue
            else:
                hem_rong_char, hem_rong = rs.group(0), rs.group(1)
                hem_rong = re.sub('mét|mét|m|,','.',hem_rong, flags=re.I)
                hem_rong = re.sub('\.+','.',hem_rong)
                hem_rong = float(hem_rong)
                return hem_rong_char, hem_rong
        else:
            return False, False

def detect_hxh(html):
    #@pr:detect_loai_hem
    p = '(?:h|hẻm|hẽm|d|đ|đường)\s{0,1}(?:xh|xe hơi|oto|ô tô)'
    rs = re.search(p, html, re.I)
    hxh_str, full_hxh = False,False
    if rs:
        span0 = rs.span(0)[0]
        pre_index = span0-30
        if pre_index<0:
            pre_index = 0
        pre = html[pre_index:span0]
        gan_sat_cach_pt = 'gần|sát|cách'
        gan_sat_cach_search = re.search(gan_sat_cach_pt,pre, re.I)
        if gan_sat_cach_search:
            return hxh_str, full_hxh
        before_index = span0 + 10
        full_hxh = html[pre_index:before_index]
        hxh_str = rs.group(0)
    return hxh_str, full_hxh

def detect_hxt(html):
    #@pr:detect_loai_hem
    p = '(?:h|hẻm|hẽm|d|đ|đường)\s{0,1}(?:xt|xe (?:tải|tãi))'
    rs = re.search(p, html, re.I)
    hxh_str, full_hxh = False,False
    if rs:
        span0 = rs.span(0)[0]
        pre_index = span0-30
        pre = html[pre_index:span0]
        gan_sat_cach_pt = 'gần|sát|cách'
        gan_sat_cach_search = re.search(gan_sat_cach_pt,pre, re.I)
        if gan_sat_cach_search:
            return hxh_str, full_hxh
        before_index = span0 + 10
        full_hxh = html[pre_index:before_index]
        hxh_str = rs.group(0)
    return hxh_str, full_hxh
    
def detect_hxm(html):
    #@pr:detect_loai_hem
    p = '(?:h|hẻm|hẽm)\s{0,1}(?:xm|xe (?:máy))'
    rs = re.search(p, html, re.I)
    hxh_str, full_hxh = False,False
    if rs:
        span0 = rs.span(0)[0]
        pre_index = span0-30
        pre = html[pre_index:span0]
        gan_sat_cach_pt = 'gần|sát|cách'
        gan_sat_cach_search = re.search(gan_sat_cach_pt,pre, re.I)
        if gan_sat_cach_search:
            return hxh_str, full_hxh
        before_index = span0 + 10
        full_hxh = html[pre_index:before_index]
        hxh_str = rs.group(0)
    return hxh_str, full_hxh
    
def detect_hbg(html):
    #@pr:detect_loai_hem
    p = '(?:h|hẻm|hẽm)\s{0,1}(?:bg|ba (?:gát|gác))'
    rs = re.search(p, html, re.I)
    hxh_str, full_hxh = False,False
    if rs:
        span0 = rs.span(0)[0]
        pre_index = span0-30
        pre = html[pre_index:span0]
        gan_sat_cach_pt = 'gần|sát|cách'
        gan_sat_cach_search = re.search(gan_sat_cach_pt,pre, re.I)
        if gan_sat_cach_search:
            return hxh_str, full_hxh
        before_index = span0 + 10
        full_hxh = html[pre_index:before_index]
        hxh_str = rs.group(0)
    return hxh_str, full_hxh


def detect_loai_hem(html):
    loai_hem_selection = False
    loai_hem, full_loai_hem = detect_hxh(html)
    if loai_hem:
        loai_hem_selection = 'hxh'
    else:
        loai_hem,  full_loai_hem = detect_hxt(html)
        if loai_hem:
            loai_hem_selection = 'hxt'
        else:
            loai_hem,  full_loai_hem = detect_hxm(html)
            if loai_hem:
                loai_hem_selection = 'hxm'
            else:
                loai_hem,  full_loai_hem = detect_hbg(html)
                if loai_hem:
                    loai_hem_selection = 'hbg'
    return full_loai_hem, loai_hem_selection

def _compute_loai_hem_combine(html):
        if not html:
            return 
        mat_tien, full_mat_tien, is_mat_tien = detect_is_mat_tien(html)
        hem_rong_char, hem_rong = detect_hem_rong(html)
        full_loai_hem, loai_hem_selection = detect_loai_hem(html)
        loai_hem_combine = loai_hem_selection
        if not loai_hem_selection:
            if is_mat_tien:
                loai_hem_combine = 'mt'
            elif hem_rong:
                if hem_rong > 10:
                    loai_hem_combine = 'mt'
                elif hem_rong >= 6:
                    loai_hem_combine = 'hxt'
                elif hem_rong >= 4:
                    loai_hem_combine = 'hxh'
                elif hem_rong >= 2.5:
                    loai_hem_combine = 'hbg'
                elif hem_rong:
                    loai_hem_combine = 'hxm'
        return mat_tien, full_mat_tien, is_mat_tien,hem_rong_char, hem_rong, full_loai_hem, loai_hem_selection, loai_hem_combine

########################### compute choosed area ###################

def tim_dien_tich_trong_bai(html):
    p ='(?:diện tích|dt|dtcn)[\W]*([1-9]+[\.,]\d+)\s*m2'
    rs = re.search(p, html, re.I)
    dt = 0
    if rs:
        dt = rs.group(1)
        dt = dt.replace(',','.')
        dt = float(dt)
    return dt

def tim_dien_tich_sd_trong_bai(html):
    dt = 0
    while 1:
        p ='(?:(?:diện tích|dt)\s*(?:sử dụng|sd|sàn|xd))[\W]*([0-9]+[\.,]*\d*)\s*m2'
        rs = re.search(p, html, re.I)
        if rs:
            span0 = rs.span(0)[0]
            span1 =  rs.span(0)[1]
            pre_index = span0-50
            if pre_index<0:
                pre_index = 0
            pre = html[pre_index:span0]
            gan_sat_cach_pt = 'gpxd|giấy phép xây dựng'
            gpxd_search = re.search(gan_sat_cach_pt,pre, re.I)
            if gpxd_search:
                before_index = span1 + 1
                html = html[before_index:]
                continue
            else:
                dt = rs.group(1)
                dt = dt.replace(',','.')
                dt = float(dt)
                return dt
        else:
            return dt

def tim_dai_rong(html):
    auto_ngang, auto_doc = 0,0
    pt= '(\d{1,3}[\.,m]{0,1}\d{0,2}) {0,1}m{0,1}(( {0,1}[x*] {0,1}))(\d{1,3}[\.,m]{0,1}\d{0,2})'
    rs = re.search(pt, html,flags = re.I)
    
    if rs:
        auto_ngang, auto_doc = float(rs.group(1).replace(',','.').replace('m','.').replace('M','.')),float(rs.group(4).replace(',','.').replace('m','.').replace('M','.'))
    elif not rs:
        pt= '(dài|rộng|ngang)[: ]{1,2}(\d{1,3}[\.,m]{0,1}\d{0,2}) {0,1}m{0,1}(([\W]{1,3}(dài|rộng|ngang)[: ]{1,2}))(\d{1,3}[\.,m]{0,1}\d{0,2})'
        rs = re.search(pt, html,flags = re.I)
        if rs:
            auto_ngang, auto_doc = float(rs.group(2).replace(',','.').replace('m','.').replace('M','.')),float(rs.group(6).replace(',','.').replace('m','.').replace('M','.'))
    return auto_ngang, auto_doc

def auto_ngang_doc_compute(html,rarea):
    auto_ngang, auto_doc = tim_dai_rong(html)
    dien_tich_trong_topic = tim_dien_tich_trong_bai(html)
    choose_area = 0
    auto_dien_tich = 0
    ti_le_dien_tich_web_vs_auto_dien_tich = 0
    if auto_ngang and auto_doc:
        auto_dien_tich = auto_ngang*auto_doc
        ti_le_dien_tich_web_vs_auto_dien_tich = rarea/auto_dien_tich
        if rarea ==0:
            choose_area = auto_dien_tich 
        elif ti_le_dien_tich_web_vs_auto_dien_tich > 1.4 and ti_le_dien_tich_web_vs_auto_dien_tich < 5:
            choose_area = auto_dien_tich
        else:
            choose_area = rarea
    else:
        choose_area = rarea or dien_tich_trong_topic
    return auto_ngang, auto_doc, auto_dien_tich, choose_area, ti_le_dien_tich_web_vs_auto_dien_tich,  dien_tich_trong_topic

def gpxd_search(pre):
    gan_sat_cach_pt = 'gpxd|giấy phép xây dựng'
    gpxd_search = re.search(gan_sat_cach_pt,pre, re.I)
    return gpxd_search

def detect_only_lau(html, pt = '(\d{1,2})\s*(?:lầu|l)(?:\W|$)'):
    while 1:
        rs = re.search(pt, html, re.I)
        so_lau = 0
        so_lau_char = False
        if rs:
            pre = previous_of_match(html, rs)
            gpxd_search_rs = gpxd_search(pre)
            if gpxd_search_rs:
                before_index = rs.span(0)[1] + 1
                html = html[before_index:]
                continue
            else:
                so_lau = rs.group(1)
                so_lau_char = rs.group(0)
                try:
                    so_lau = int(so_lau)
                except:
                    so_lau = 0
                return so_lau, so_lau_char
        else:
            return so_lau, so_lau_char

def detect_lung_only(html, pt = 'lửng|lững'):
    while 1:
        is_lung = False
        rs = re.search(pt, html, re.I)
        so_lau = 0
        so_lau_char = False
        if rs:
            pre = previous_of_match(html, rs)
            gpxd_search_rs = gpxd_search(pre)
            if gpxd_search_rs:
                before_index = rs.span(0)[1] + 1
                html = html[before_index:]
                continue
            else:
                is_lung = True
                return is_lung
        else:
            return is_lung

def detect_lau_tranh_gpxd(html):
    so_lau, so_lau_char = detect_only_lau(html)
    if not so_lau:
        so_lau, so_lau_char = detect_only_lau(html, pt = '(\d{1,2})\s*(?:tầng)(?:\W|$)')
        if so_lau:
            so_lau = so_lau -1
    so_lau_he_so = so_lau
    is_lung = detect_lung_only(html)
    if is_lung:
        so_lau +=0.5
        so_lau_he_so +=0.7

    is_st = detect_lung_only(html, pt = 'sân thượng')
    if is_st:
        so_lau +=1
        so_lau_he_so +=0.5
    return so_lau, so_lau_char, so_lau_he_so

def detect_lau(html):
    pt = '(\d{1,2})\s*(?:lầu|l)(?:\W|$)'
    rs = re.search(pt, html, re.I)
    so_lau = 0
    so_lau_char = False
    
    if rs:
        so_lau = rs.group(1)
        so_lau_char = rs.group(0)
        try:
            so_lau = int(so_lau)
        except:
            so_lau = 0
    else:
        pt = '(\d{1,2})\s*(?:tầng)(?:\W|$)'
        rs = re.search(pt, html, re.I)
        if rs:
            so_lau = rs.group(1)
            so_lau_char = rs.group(0)
            try:
                so_lau = int(so_lau)
            except:
                so_lau = 0
        else:
            pt = '(cấp 4|c4|c4)\W'
            rs = re.search(pt, html, re.I)
            if rs:
                so_lau = 0.1
                so_lau_char = rs.group(1)


                
    so_lau_he_so = so_lau
    pt = 'lửng|lững'
    rs = re.search(pt, html, re.I)
    if rs:
        so_lau +=0.5
        so_lau_he_so +=0.7

    pt = 'sân thượng'
    rs = re.search(pt, html, re.I)
    if rs:
        so_lau +=1
        so_lau_he_so +=0.5

    return so_lau, so_lau_char, so_lau_he_so

def _compute_muc_gia(gia):
        muc_gia_list = [('0','0'),('<1','<1'),('1-2','1-2'),('2-3','2-3'),
            ('3-4','3-4'),('4-5','4-5'),('5-6','5-6'),('6-7','6-7'),('7-8','7-8'),('8-9','8-9'),('9-10','9-10'),('10-11','10-11'),('11-12','11-12'),('>12','>12')]
        selection = None
        for muc_gia_can_tren in range(0,len(muc_gia_list)):
            if gia <= muc_gia_can_tren:
                selection = muc_gia_list[muc_gia_can_tren][0]
                break
        if not selection:
            selection = muc_gia_list[-1][0]
        return selection

def muc_don_gia_(don_gia):
    muc_dt_list =[('0','0'),('0-30','0-30'),('30-60','30-60'),('60-90','60-90'),
                                ('90-120','90-120'),('120-150','120-150'),('150-180','150-180'),('180-210','180-210'),('>210','>210')]
    selection = None
    for muc_gia_can_tren in range(0,8):
        if don_gia <= muc_gia_can_tren*30:
            selection = muc_dt_list[muc_gia_can_tren][0]
            break
    if not selection:
        selection = muc_dt_list[-1][0]
    return selection

def muc_ti_le_don_gia_(ti_le_don_gia):
    muc_dt_list =[('0','0'), ('0-0.4','0-0.4'),('0.4-0.8','0.4-0.8'),('0.8-1.2','0.8-1.2'),
                                ('1.2-1.6','1.2-1.6'), ('1.6-2.0','1.6-2.0'), ('2.0-2.4','2.0-2.4'), ('2.4-2.8','2.4-2.8'), ('>2.8','>2.8')]
    selection = None
    for muc_gia_can_tren in range(0,8):
        if ti_le_don_gia <= muc_gia_can_tren*0.4:
            selection = muc_dt_list[muc_gia_can_tren][0]
            break
    if not selection:
        selection = muc_dt_list[-1][0]
    return selection
    
def _muc_dt(choose_area):
        muc_dt_list = [('0','0'), ('<10','<10'),('10-20','10-20'),('20-30','20-30'),('30-40','30-40'),('40-50','40-50'),('50-60','50-60'),('60-70','60-70'),('>70','>70')]
        selection = None
        for muc_gia_can_tren in range(0,8):
            if choose_area <= muc_gia_can_tren*10:
                selection = muc_dt_list[muc_gia_can_tren][0]
                break
        if not selection:
            selection = muc_dt_list[-1][0]
        return selection

def _compute_choosed_area_muc_gia(html, gia, area, district_id, loai_hem_combine):
        auto_ngang, auto_doc, auto_dien_tich, choose_area, ti_le_dien_tich_web_vs_auto_dien_tich,  dien_tich_trong_topic = \
                auto_ngang_doc_compute(html, area)
        dtsd = tim_dien_tich_sd_trong_bai(html)
        so_lau, so_lau_char, so_lau_he_so =  detect_lau_tranh_gpxd(html)
        ti_le_dtsd = False
        dtsd_tu_so_lau = 0
        dtsd_he_so_lau = 0

        allow_loop = 2
        while allow_loop:
            allow_loop -=1
            if so_lau:
                dtsd_tu_so_lau = (so_lau + 1) * choose_area * 0.9
                dtsd_he_so_lau = (so_lau_he_so + 1) * choose_area * 0.9 #để tính tiền xác nhà 
                if so_lau_he_so < 2:
                    dtsd_he_so_lau = dtsd_he_so_lau * 0.5# để tính tiền xác nhà
                if dtsd and choose_area:
                    ti_le_dtsd = dtsd_tu_so_lau / dtsd
            dtsd_combine = dtsd or dtsd_tu_so_lau
            dtsd_combine_he_so_lau = dtsd_he_so_lau or dtsd
            if not dtsd_combine_he_so_lau:
                dtsd_combine_he_so_lau =  choose_area * 0.5
            gia_xac_nha = dtsd_combine_he_so_lau * 0.006
            
            gia_dat_con_lai = 0
            don_gia_dat_con_lai = 0
            
            ti_le_gia_dat_con_lai_gia = 0
            if gia > 0.2 and gia_xac_nha:
                gia_dat_con_lai = gia - gia_xac_nha
                ti_le_gia_dat_con_lai_gia = gia_dat_con_lai/gia
                if ti_le_gia_dat_con_lai_gia  < 0.5:
                    gia_dat_con_lai = gia
                    ti_le_gia_dat_con_lai_gia = gia_dat_con_lai/gia
                if choose_area:
                    don_gia_dat_con_lai = 1000 * gia_dat_con_lai / choose_area
            
            
            don_gia = 0
            if gia > 0.5 and choose_area:
                don_gia = gia*1000/choose_area

            # muc gia quan vao day
            don_gia_quan = 0
            ti_le_don_gia_dat_con_lai = 0

            if loai_hem_combine and don_gia_dat_con_lai:
                if loai_hem_combine =='mt':
                    loai_hem_combine = 'mat_tien'
                else:
                    loai_hem_combine = loai_hem_combine
                attr = 'don_gia_%s'%loai_hem_combine
                

                if district_id:
                    don_gia_quan = getattr(district_id, attr)
                    if not don_gia_quan:
                        don_gia_quan = getattr(district_id, attr + '_tc')

            
            if not don_gia_quan and district_id:
                don_gia_quan = district_id.muc_gia_quan or district_id.don_gia_hbg_tc

            if don_gia_quan:
                ti_le_don_gia_dat_con_lai = don_gia_dat_con_lai/don_gia_quan

            if ti_le_don_gia_dat_con_lai != 0 and ti_le_don_gia_dat_con_lai < 0.3:
                if choose_area and so_lau:
                    choose_area = choose_area/(so_lau + 1) # cho lập lại khi choose_area được gán lại
                    continue
                else:
                    break
            else:
                break

        ti_le_don_gia = ti_le_don_gia_dat_con_lai
        muc_ti_le_don_gia = muc_ti_le_don_gia_(ti_le_don_gia)   
        muc_don_gia = muc_don_gia_(don_gia)  
        muc_dt = _muc_dt(choose_area)
        muc_gia = _compute_muc_gia(gia)

        return don_gia_quan, ti_le_don_gia_dat_con_lai, ti_le_don_gia, \
            auto_ngang, auto_doc, auto_dien_tich, ti_le_dien_tich_web_vs_auto_dien_tich, \
            dtsd, choose_area, so_lau, so_lau_char, so_lau_he_so,\
            dtsd_tu_so_lau, ti_le_dtsd, dtsd_combine, gia_xac_nha,\
            gia_dat_con_lai, don_gia_dat_con_lai, don_gia, muc_don_gia,\
            muc_ti_le_don_gia, muc_dt, muc_gia, ti_le_gia_dat_con_lai_gia



######################### !compute function ###############




def valid_fetch_list(rs):
    shows = ['gia_dat_con_lai']
    for i in ['public_date', 'public_datetime',  'area_name', 'region_name', 'price', 'gia','mat_tien_or_trich_dia_chi','gia_dat_con_lai']:
        print ('**%s**'%i)
        filter_rs = list(filter(lambda r: r[i], rs))
        print (len(filter_rs))
        if i =='mat_tien_or_trich_dia_chi':
            for r in filter_rs:
                print ('mat_tien_or_trich_dia_chi', r['link'])
                print ('mat_tien_or_trich_dia_chi', r['mat_tien_or_trich_dia_chi'])
        if i in shows:
            for j in filter_rs:
                print (i, j[i], j['link'], j['ti_le_don_gia_dat_con_lai'],j['ti_le_gia_dat_con_lai_gia'])
        



    # print ('**not gia**')
    # filter_rs = list(filter(lambda r: not r['gia'], rs))
    # print (len(filter_rs))

def test_fetch(begin_page = 1, end_page=1):
    set_attrs_dict_for_test = {}
    site_name = 'chotot'
    site_name = 'muaban'
    site_name = 'cuahangtaphoa'
    site_name = 'batdongsan'
    site_name = 'chotot'
    is_test = True
    is_save_mau = True
    topic_path = False
    topic_link = False
    page_path = False
    page_link = False
    
    set_attrs_dict_for_test.update({'is_test':is_test, 'site_name': site_name, 'is_save_mau':is_save_mau})
    if site_name == 'chotot':
        page_path = 'page_chotot'
        # topic_link = 'https://gateway.chotot.com/v1/public/ad-listing/73970343'
        # topic_link = 'https://gateway.chotot.com/v1/public/ad-listing/76138717'
        # topic_path = 'mau/topic_chotot_50_50'
        more_dict = { 'url':'https://gateway.chotot.com/v1/public/ad-listing?cg=1000&limit=20&st=s,k',
        'begin_page':1,  'end_page':5 }
    elif site_name =='batdongsan':
        more_dict = { 'url':'https://batdongsan.com.vn/nha-dat-ban',
        'begin_page':500,  'end_page':500,  'topic_path':'mau/file_topic_bug_theo_y_muon_batdongsan'}
        # more_dict = {'is_test':True, 'site_name': 'batdongsan', 'page_path':'mau/bds_page_loai_2',
        # 'st_is_request_topic':False, }
        more_dict = {'url':'https://batdongsan.com.vn/nha-dat-ban',
        'begin_page':1,  'end_page':1, }# 'is_save_and_raise_in_topic':True
    
        # more_dict = {'is_test':True, 'site_name': 'batdongsan', 'url':'https://batdongsan.com.vn/nha-dat-ban',
        # 'begin_page':500,  'end_page':500,  'topic_link':'https://batdongsan.com.vn/ban-can-ho-chung-cu-duong-ho-tung-mau-phuong-phu-dien-prj-goldmark-city/-bay-gio-hoac-khong-bao-gio-mua-160m2-cho-gia-dinh-da-the-he-tang-ngay-hon-600-000-000-pr26721510'
        # }
    elif site_name =='muaban':
        more_dict = { 'url':'https://muaban.net/ban-nha-ho-chi-minh-l59-c32?cp=14' }
    elif site_name =='cuahangtaphoa':
        more_dict = { 'url':'http://www.cuahangtaphoa.com/page-6-cua-hang-tap-hoa.html' }

    set_attrs_dict_for_test.update(more_dict)
    set_attrs_dict_for_test['topic_path']=topic_path
    set_attrs_dict_for_test['topic_link']=topic_link
    set_attrs_dict_for_test['page_path']=page_path
    set_attrs_dict_for_test['page_link']=page_link
    set_attrs_dict_for_test['begin_page']=begin_page
    set_attrs_dict_for_test['end_page']=end_page


    main_fetch = MainFetchCommon(set_attrs_dict_for_test = set_attrs_dict_for_test)
    fetch_list = main_fetch.fetch_a_url_id(False)
    if site_name in ['chotot','batdongsan','cuahangtaphoa']:
        valid_fetch_list(fetch_list)

def test_trich_dia_chi():
    html = 'bán nhà 26/3 200m'
    html = '''cần bán những căn nhà sau: (: :địa chỉ bên dưới thật 100%) .nhà thứ 1) hẻm xe hơi số 67/4b hoàng hoa thám p6 bình thạnh , nhà gồm lầu đúc mới , gồm 2pn,2Wc, giá 3,25 tỷ( sổ hồng bao sang tên),,,,,,,,,,,,...nhà thứ 1) số 62/7/29. Trần bình trọng p5 bình Thạnh: diện tích: ngang 3,5 m dài 18m / gồm 3 lầu đúc mới, giá :4,3 tỷ ( sổ Hồng) .........cần bán 2 lô đất số 273/40..nguyễn văn đậu , giá :6,1 tỷ/lô , còn 2 lô ( hình bên dưới) .................chú ý: địa chỉ dưới đây thật 100% :*) nhà bán hẻm xe hơi số 97/13 nguyễn bỉnh khiêm ( gần phạm văn đồng và lê quang định) , diện tích ngang 3m dài 12m/ 1 lầu , giá: 2,15 tỷ ...........nhà bán thứ 1) số 361/35 lê quang định , quận bình thạnh , dtsd : gần 20m2 / gồm lầu mới giá: 1,05 tỷ ( sổ hồng.).........nhà bán thứ.4) : hẻm xe hơi số 220/52 hoàng hoa thám / nhà gồm 2 lầu đúc mới , giá 2,75 tỷ ....,;căn bán thứ 4) : hẻm 251/92/4 lê quang định p7 bình thạnh, dtsd:30m2/ gồm 2 lầu đúc mới giá: 1,5 tỷ (sổ hồng).....................căn bán thứ 5)..giá bán 4,7 tỷ/ nhà số 170 Nguyễn văn đậu p7 bình thạnh ( đầu trần bình trọng ) ngang 7m dài 6m / 2 lầu và sân thương..;................nhà bán thứ 6) số 106/9/8 lương Ngọc quyến , nhà gồm 2 lầu , giá : 1,45 tỷ ............................. [email protected]) cần bán những căn nhà sau: Nhà bán thứ 8) số 207 đường bạch đằng p15 bình thạnh, dtsd: 42m2, giá: 3,8 tỷ ( sổ hồng) ... @) .. nhà bán 9) số 395/30 Lê quang định p5 bình thạnh, nhà gồm lầu mới, dtsd:25m2; giá 1,35 tỷ ( sổ hồng).. , khu dân cư văn minh, có trí thức, rất an ninh, .....mong tiếp khách thiện chí...hình dưới đây thật 100%................Lh: 0906975079 / tùng hoặc lh : 1/9c trần bình trọng p5 bình thạnh. nhận ký gửi , mua bán , hợp thức hóa ,kê khai di sản thừa kế, nhận làm đơn khiếu nại, khiếu kiện, nhận làm dv hôn nhân, nhận đại diện ủy quyền tại tòa.: về vụ việc: dân sự , hình sự, hành chính...............'''
    html = 'bán nhà 10 Ho, bán nhà 23 Ba Đọ av , 15/32 hoa thi buoi abc a  d d 32/35 chi do'
    rs = _compute_mat_tien_or_trich_dia_chi1 (False, html, html)
    print (rs)

if __name__ == '__main__':
    loai_test = 'trich_dia_chi'
    loai_test = 'test_fetch'
    if loai_test == 'trich_dia_chi':
        test_trich_dia_chi()
    else:
        # jobs = []
        # nth = 2
        # part = 1
        # for i_thread in range(nth):
        #     begin = i_thread* part + 1
        #     end = (i_thread + 1) * part
        #     p = multiprocessing.Process(target=test_fetch, args=(begin, end))
        #     jobs.append(p)
        #     p.start()
        test_fetch()
    

    
    





