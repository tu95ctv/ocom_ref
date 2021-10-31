from ast import literal_eval
attrs_str = '''{'class': 'btnS', 'href': 'javascript:HistoryBack()', 'onmouseover': "window.status='戻る';return true", 'onmousemove': "window.status='戻る';return true", 'onmouseout': "window.status='';return true"}'''
attrs_str = '''{'href': '#', 'onclick': "pbiExec('/indexPbi.jsp')", 'onmouseover': "window.status='入札情報サービス';return true", 'onmousemove': "window.status='入札情報サービス';return true", 'onmouseout': "window.status='';return true"}'''
# rs = literal_eval(str)
# print (type(rs))




# rs = [attr_to_xpath(i) for i in rs.items()]
# print (rs)
# print (rs[1])
# rs3 = ''.join(rs)
# rs3 = '//*'+rs3
# print (rs3)

# def attr_to_xpath(attr):
#     key, val = attr
#     return f'[@{key}="{val}"]'

# def attrs_to_xpath(attrs_str):
#     attrs_dict = literal_eval(attrs_str)
#     return '//*' + ''.join([f'[@{k}="{v}"]' for k,v in attrs_dict.items()])

# rs3 = attrs_to_xpath(attrs_str)
# print ('rs3', rs3)
####
f.close()
from lxml import etree, html
f=open(r'C:\Users\nguye\Desktop\crawler\2.html','r', encoding="utf-8")
rs = f.read()
parser = html.HTMLParser(recover=True, encoding='utf-8')
x = etree.fromstring(rs, parser=parser)
rs = x.xpath("//*[@onload='autoStart']")
# rs = x.xpath("//*[@action='/ebidPPIPublish/EjPPIj']")
x.xpath("//body[@onload='autoStart()']//a[@onclick='document.frm.submit();']")
x.xpath("//body[@onload='autoStart()']//a[@onclick='document.frm.submit()']")

x.xpath("//body[@onload='autoStart()']//a[@onclick='document.frm.submit()'][text()]")
x.xpath("//body[@onload='autoStart()']//a[contains(@onclick,'document.frm.submit()')]")


f.close()
# rs = x.xpath(rs3)
# e=rs[0]
# print (e)