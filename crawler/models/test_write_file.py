import re
a = '''Babel           2.3.4	
beautifulsoup4  4.10.0	
certifi         2021.5.30	
cffi            1.14.6	
chardet         3.0.4	
decorator       4.0.10	
docutils        0.12	
ebaysdk         2.1.5	
feedparser      6.0.8	
gevent          1.5.0	
greenlet        0.4.14	
html2text       2016.9.19	
idna            2.7	
Jinja2          2.10.1	
libsass         0.12.3	
lxml            4.6.3	
Mako            1.0.4	
MarkupSafe      0.23	
mock            2.0.0	
num2words       0.5.6	
ofxparse        0.16	
passlib         1.7.2	
pbr             5.6.0	
Pillow          8.3.2	
pip             21.2.4	
psutil          5.6.3	
psycopg2        2.9.1	
pycparser       2.20	
pydot           1.2.3	
pyparsing       2.1.10	
PyPDF2          1.26.0	
pypiwin32       223	
pyserial        3.1.1	
python-dateutil 2.5.3	
pytz            2016.7	
pyusb           1.0.0	
pywin32         301	
qrcode          5.3	
reportlab       3.6.1	
requests        2.20.0	
setuptools      58.0.4	
sgmllib3k       1.0.0	
six             1.16.0	
soupsieve       2.2.1	
urllib3         1.24.3	
vatnumber       1.0	
vobject         0.9.3	
Werkzeug        0.16.0	
xlrd            1.0.0	
XlsxWriter      0.9.3	
xlwt            1.3.0	
'''

r = re.sub(' +','==',a)
print (r)
with open(r'C:\d4\tu_code_odoo\ocom_ref\crawler\models\requirement.txt','w') as f:
    print ('req')
    f.write(r)
