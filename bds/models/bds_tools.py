# -*- coding: utf-8 -*-
from time import sleep
from urllib import request
from odoo import fields
from odoo.osv import expression
import datetime
from unidecode import unidecode
import os
import logging
import json
_logger = logging.getLogger(__name__)

class FetchError(Exception):
    pass

class SaveAndRaiseException(Exception):
    pass

class SaveAndPass(Exception):
    pass

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
    domain = expression.AND([domain_not_active, domain])
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
                if isinstance(domain_val, datetime.date):
                    exit_val = fields.Date.from_string(exit_val)
                if exit_val !=domain_val:
                    is_change = True
                    break
        if is_change:
            searched_object.write(create_write_dict)
    return return_obj       

def save_to_disk( ct, name_file ):
    path = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(path,'%s.html'%name_file), 'w')
    f.write(ct)
    f.close()

def file_from_tuong_doi(tuong_doi_path):
    path = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(path,'%s.html'%tuong_doi_path), 'r')
    return f.read()


def convert_text_to_json(value):
    if value:
        value = value.replace("'",'"')
        value = json.loads(value)
    else:
        value = {}
    return value

