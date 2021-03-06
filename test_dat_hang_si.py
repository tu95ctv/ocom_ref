import requests
import re
from lxml import etree, html
import re
import json
HEADERS = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36' }

def read_file(p):
    f = open(p,'r', encoding='utf-8')
    rs = f.read()
    f.close()
    return rs

def get_form_inputs(content, xpath="//form[@id='frm_indexs']//input|//form[@id='frm_indexs']//select"):
    parser = html.HTMLParser(recover=True, encoding='utf-8')
    x = etree.fromstring(content, parser=parser)
    rs2 = x.xpath(xpath)
    # rs2 = form.xpath('.//input|.//select')
    rs2 = [(i.get('name'),i.get('value')) for i in rs2]
    rs2 = dict(rs2)
    # print ('**get_form_inputs**', rs2)
    return rs2

def request_and_save(u,p=None,data={}, headers=None, cookies=None):
    if data:
        m = requests.post
    else:
        m = requests.get
    response_object = m(u, data=data, headers=headers, cookies=cookies)
    headers = response_object.headers
    s = response_object.content.decode('utf-8')
    if p:
        f = open(p,'w', encoding='utf-8')
        f.write(s)
        f.close()
    return headers, s

def login():
    login_u = 'https://dathangsi.vn/login.html'
    # p = r'C:\Users\nguye\Desktop\crawler\login.html'
    d = {'username':'ndt', 'password':'1'}
    response_headers,_ = request_and_save(login_u, None, headers=HEADERS, data=d)
    return response_headers
# response_headers = login()
def get_cookies(response_headers, only_token=False):
    Set_Cookie = response_headers['Set-Cookie']
    if only_token:
        rs = re.search('PHPSESSID=(.*?);',Set_Cookie)
        PHPSESSID = rs.group(1)
        cookies={'PHPSESSID':PHPSESSID}
    else:
        ck = Set_Cookie.split(';')
        cookies = dict([i.strip().split('=',1) for i in ck])
    # print ('cookies',cookies)
    return cookies
# cookies = get_cookies(response_headers)
u = 'https://dathangsi.vn/9606-bo-5-quan-lot-muji-.html'
def get_data_1_sp(u,is_save=None):
    p = is_save and  r'C:\Users\nguye\Desktop\crawler\product.html'
    h,c = request_and_save(u, p)
    rs = get_form_inputs(c)
    print ('get_form_inputs', rs)
    return rs
#dat hang
data_giay = {'amount7220':2,
'option_name7220':'M???c ?????nh',
'checkbox_id[]':7220,
'news_id':7213,
'submit':'Mua ngay'}

data_ao_mua = {
    'amount7445':1,
'option_name7445':'M???c ?????nh',
'checkbox_id[]':'7445',
'submit':'Mua ngay',
'news_id':'7438',
}

def dat_hang(data):
    u = 'https://dathangsi.vn/addcart.html' 
    p_addcard = r'C:\Users\nguye\Desktop\crawler\addcard.html'
    request_and_save(u, p_addcard, headers=HEADERS, cookies=cookies, data=data)
    print ('?????t h??ng xong')

# dat_hang(data_giay)
# dat_hang(data_ao_mua)

def luu_shopcart():
    p_shopcart = r'C:\Users\nguye\Desktop\crawler\shopcart.html'
    u='https://dathangsi.vn/shopcart.php?display=1'
    print ('p_shopcart', p_shopcart)
    return request_and_save(u, p_shopcart, headers=HEADERS, cookies=cookies)



def convert_to_postman_data(rs2):
    rs2 = rs2.items()
    out= ''
    for i in rs2:
        if i[0]:
            out += str(i[0]) +':' + str(i[1]) + '\n'
    return out

# h,content = luu_shopcart()
# rs1 = get_form_inputs(content,'//input')

def mua_hang():
    u = 'https://dathangsi.vn/shopping/shopping.html'
    p_shopping = r'C:\Users\nguye\Desktop\crawler\shopping.html'
    headers, content =\
        request_and_save(u, p_shopping, headers=HEADERS, cookies=cookies, data={})
    rs2 = get_form_inputs(content)
    print ('rs1 in mua hang', rs1)
    rs2.update(rs1)
    rs2.update({'namecity':1, 'district':15, 'address':'13 Truong Hoang Thanh'})
    # print ('rs2', rs2)
    rs2.update({'tong_tien_cat':11000})
    u = 'https://dathangsi.vn/cartdetail.html'
    p_card_deatail = r'C:\Users\nguye\Desktop\crawler\card_detail.html'
    headers, content =\
        request_and_save(u, p_card_deatail, headers=HEADERS, cookies=cookies, data=rs2)
    out = convert_to_postman_data(rs2)
    # print ('**out**', out)
    return rs2

def get_payment(is_payment=True):
    p_payment = r'C:\Users\nguye\Desktop\crawler\get_payment.html'
    u = 'https://dathangsi.vn/payment.html'
    headers, content =\
        request_and_save(u, p_payment, headers=HEADERS, cookies=cookies, data={})
    rs3 = get_form_inputs(content, xpath="//form[@id='frm_indexs_2']//input|//form[@id='frm_indexs_2']//select")
    del rs3['button_del']
    p_after_payment = r'C:\Users\nguye\Desktop\crawler\after_payment.html'
    print ('**rs3***',rs3)
    if is_payment:
        headers, content =\
            request_and_save(u, p_after_payment, headers=HEADERS, cookies=cookies, data=rs3)
        print ('???? ?????t h??ng')
    print ('*p_payment**', p_payment)
# mua_hang()
# get_payment()

def get_link_session_id():
    f=open(r'C:\Users\nguye\Desktop\crawler\shopcart.html','r', encoding="utf-8")
    rs = f.read()
    f.close()
    parser = html.HTMLParser(recover=True, encoding='utf-8')
    x = etree.fromstring(rs, parser=parser)
    rs2 = x.xpath("//*[contains(@onchange,'update_amount')]")
    rs3 = [i.get('onchange') for i in rs2]
    rs = [re.search('\((.*),', i).group(1) for i in rs3]
    print (rs)
    return rs

def etree_a_source(p):
    f=open(p,'r', encoding="utf-8")
    rs = f.read()
    f.close()
    parser = html.HTMLParser(recover=True, encoding='utf-8')
    x = etree.fromstring(rs, parser=parser)
    rs2 = x.xpath("//div[@class='gia_si_pro']")
    print (len(rs2))
    return rs2

# rs = get_link_session_id()
def delete(session_id):
    p_shopcart = r'C:\Users\nguye\Desktop\crawler\shopcart.html'
    if not isinstance(session_id,list):
        session_id = [session_id]
    for session_id in session_id:
        deletelink = 'https://dathangsi.vn/shopcart.php?delete=delete&session_id='+session_id
        p_deletelink= p_shopcart#r'C:\Users\nguye\Desktop\crawler\deletelink.html'
        request_and_save(deletelink, p_deletelink, headers=HEADERS, cookies=cookies)

def save_file(p, c):
    f = open(p,'w', encoding='utf-8')
    f.write(c)
    f.close()

def save_cookies(c):
    c = json.dumps(c)
    p = r'C:\Users\nguye\Desktop\crawler\cookies.json'
    save_file(p,c)

def load_cookies():
    p = r'C:\Users\nguye\Desktop\crawler\cookies.json'
    c = read_file(p)
    cookies = json.loads(c)
    return cookies


def lay_file_chinh():
    u = 'https://dathangsi.vn/san-pham.html'
    path = r'C:\Users\nguye\Desktop\crawler\tat_ca_san_pham.html'
    # d = {'username':'ndt', 'password':'1'}
    response_headers,_ = request_and_save(u, path, headers=HEADERS)
    return response_headers

    # def favorite():
    #     {
    #             ajaxLoad('https://dathangsi.vn/favourite.php?product_id='+product_id,'id_favourite');
    #         }

def lay_hang_ton_kho():
    u = 'https://dathangsi.vn/bangia/shop_quantity.php'
    path = r'C:\Users\nguye\Desktop\crawler\hangtonkho.xls'
    headers, content =\
        request_and_save(u, path, headers=HEADERS, cookies=cookies)
import xlrd
def doc_hang_ton_kho_tu_o_cung_xls(path):
    path = r'C:\Users\nguye\Desktop\crawler\hangtonkho.xls'
    book = xlrd.open_workbook( path )
    sh = book.sheet_by_index(0)
    print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
    # print("Cell D30 is {0}".format(sh.cell_value(rowx=29, colx=3)))
    for rx in range(sh.nrows):

        print(sh.row(rx))
def doc_hang_ton_kho_tu_o_cung_xls(path):
    path = r'C:\Users\nguye\Desktop\crawler\hangtonkho.xls'
    fr = read_file(path)
    book = xlrd.open_workbook(file_contents=fr )
    sh = book.sheet_by_index(0)
    print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
    # print("Cell D30 is {0}".format(sh.cell_value(rowx=29, colx=3)))
    for rx in range(sh.nrows):
        print(sh.row(rx))


import openpyxl
def read_one_file_openpyxl(path):
    from datetime import datetime
    content = ''
    content
    # df = pd.read_excel(path, sheet_name=None, header=None)
    wb_obj = openpyxl.load_workbook(path)
    print ('wb_obj.worksheets',wb_obj.worksheets)

import pandas as pd
def read_one_file_pd(path):
    from datetime import datetime
    content = ''
    df = pd.read_excel(path, sheet_name=None, header=None, engine='xlrd')
    # df = _process(path)
    for key, value in df.items():
        data_list = value.fillna('').values.tolist()
        for row in data_list:
            for col in row:
                if isinstance(col, datetime):
                    try:
                        row[row.index(col)] = col.strftime("%Y/%m/%d")
                    except:
                        row[row.index(col)] = str(col)
                else:
                    row[row.index(col)] = str(col)
            content += ' '.join(row) + '\n'
    return content
path = r'C:\Users\nguye\Desktop\crawler\hangtonkho.xls'
if __name__ == "__main__":
    # response_headers = login()
    # cookies = get_cookies(response_headers)
    # lay_hang_ton_kho()
    doc_hang_ton_kho_tu_o_cung_xls(1)
    # read_one_file_pd(path)
    # read_one_file_openpyxl(path)
    # # save_cookies(cookies)
    # # cookies = load_cookies()
    # print ('**cookies**', cookies)
    # u1 = 'https://dathangsi.vn/9606-bo-5-quan-lot-muji-.html'
    # d1 = get_data_1_sp(u1)
    # u2 = 'https://dathangsi.vn/8381-vi-da-nam-deabolar-.html'
    # d2 = get_data_1_sp(u2)
    # dat_hang(d1)
    # dat_hang(d1)
    # dat_hang(d2)
    # # dat_hang(d2)
    # h,content = luu_shopcart()
    # rs1 = get_form_inputs(content,'//input')
    # mua_hang()
    # get_payment(1)
    # lay_file_chinh()
    # p = r'C:\Users\nguye\Desktop\crawler\tat_ca_san_pham.html'
    # r = etree_a_source(p)
    # r0 = r[0]
    # rs =r0.xpath('.//h3')[0]
    # h3 = rs.text
    # print (h3)


