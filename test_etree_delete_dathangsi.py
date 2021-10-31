from lxml import etree, html
import re
f=open(r'C:\Users\nguye\Desktop\crawler\shopcart.html','r', encoding="utf-8")
rs = f.read()
parser = html.HTMLParser(recover=True, encoding='utf-8')
x = etree.fromstring(rs, parser=parser)
# <a href="https://dathangsi.vn/7438-giay-a5-excel-70gsm.html" target="_blank">
# 			 <img src="https://dathangsi.vn/upload/products/2019/06/06_0959-28a5e77452cfb791eede.jpg" height="90" width="90" align="center"></a>
# rs = x.xpath("//a[@href='https://dathangsi.vn/7438-giay-a5-excel-70gsm.html']")[0]

# tds = x.xpath("//td")
# for td in tds:
#     rs = td.xpath("./descendant::a[@href='https://dathangsi.vn/7438-giay-a5-excel-70gsm.html']")
#     # rs = td.xpath("./descendant::a")
#     print ('td', td,'a', rs)
#     if rs:
#         print ('akaka')
#         print (etree.tostring(td, encoding='unicode'))
        
#         print ('td parent', rs[0].xpath('./ancestor::td'))
#         if td.xpath("./input[contains(text(),'update_amount')]"):
#             print ('herrrrrrrrrrrrre')
#             raise ValueError('duma')


rs2 = x.xpath("//*[contains(@onchange,'update_amount')]")
rs3 = [i.get('onchange') for i in rs2]
rs = [re.search('\((.*),', i).group(1) for i in rs3]
print (rs)


def get_link_session_id():
    f=open(r'C:\Users\nguye\Desktop\crawler\shopcart.html','r', encoding="utf-8")
    rs = f.read()
    parser = html.HTMLParser(recover=True, encoding='utf-8')
    x = etree.fromstring(rs, parser=parser)
    rs2 = x.xpath("//*[contains(@onchange,'update_amount')]")
    rs3 = [i.get('onchange') for i in rs2]
    rs = [re.search('\((.*),', i).group(1) for i in rs3]
    return rs

def get_form_inputs():
    f=open(r'C:\Users\nguye\Desktop\crawler\shopping.html','r', encoding="utf-8")
    rs = f.read()
    # parser = html.HTMLParser(recover=True, encoding='utf-8')
    x = etree.fromstring(rs, parser=parser)
    form = x.xpath("//form[@id='frm_indexs']")[0]
    # print (etree.tostring(form, encoding='unicode'))
    rs2 = form.xpath('.//input|.//select')
    rs2 = [(i.get('name'),i.get('value')) for i in rs2]
    print (rs2)
    out= ''
    for i in rs2:
        if i[0]:
            out += str(i[0]) +':' + str(i[1]) + '\n'
    # rs3 = [i.get('onchange') for i in rs2]
    # rs = [re.search('\((.*),', i).group(1) for i in rs3]
    print (out)
    return rs2


def get_form_inputs_payment():
    f=open(r'C:\Users\nguye\Desktop\crawler\payment.html','r', encoding="utf-8")
    rs = f.read()
    # parser = html.HTMLParser(recover=True, encoding='utf-8')
    x = etree.fromstring(rs, parser=parser)
    form = x.xpath("//form[@id='frm_indexs_2']")[0]
    # print (etree.tostring(form, encoding='unicode'))
    rs2 = form.xpath('.//input|.//select')
    rs2 = [(i.get('name'),i.get('value')) for i in rs2]
    print (rs2)
    out= ''
    for i in rs2:
        if i[0]:
            out += str(i[0]) +':' + str(i[1]) + '\n'
    # rs3 = [i.get('onchange') for i in rs2]
    # rs = [re.search('\((.*),', i).group(1) for i in rs3]
    print (out)
    return rs2


def get_form_inputs_muangay():
    f=open(r'C:\Users\nguye\Desktop\crawler\muangay_bangkeo.html','r', encoding="utf-8")#130
    rs = f.read()
    # parser = html.HTMLParser(recover=True, encoding='utf-8')
    x = etree.fromstring(rs, parser=parser)
    form = x.xpath("//form[@id='frm_indexs']")[0]
    # print (etree.tostring(form, encoding='unicode'))
    rs2 = form.xpath('.//input|.//select')
    rs2 = [(i.get('name'),i.get('value')) for i in rs2]
    print (rs2)
    out= ''
    for i in rs2:
        if i[0]:
            out += str(i[0]) +':' + str(i[1]) + '\n'
    # rs3 = [i.get('onchange') for i in rs2]
    # rs = [re.search('\((.*),', i).group(1) for i in rs3]
    print (out)
    return rs2


rs = get_form_inputs_muangay()
