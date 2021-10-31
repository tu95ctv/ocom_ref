# -*- coding: utf-8 -*-
import re
from urllib.request import Request
import requests
url = "https://chotatsu2.pref.hiroshima.lg.jp/ebidPPIPublish/EjPPIt"
url = 'https://www.cals.pref.yamanashi.lg.jp/'
url = 'http://kuma-cocoro.jp'
# url = 'http://abc.jp'

# url = 'https://ppi.keiyaku.city.hiroshima.lg.jp/PPI_P/'
headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'} 
headers  = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
        }
# request=Request(url,None,headers) #The assembled request
# response = urlopen(request)
# data = response.read().decode('utf-8') # The data u need
# print(data)

rs = requests.get(url, timeout=3, headers=headers)
content_type = rs.headers.get('Content-Type')
import brotli
content = rs.content
# content = brotli.decompress(content)

charset_decode = 'utf-8'
try:
    charset = content_type.split(';')[1].split('=')[1]
    charset = charset.lower()
    if charset in ['ms932','windows-31j']:
        charset_decode = 'shift_jis'
    else:
        charset_decode = charset
except:
    pass
try:
    out = content.decode(charset_decode)
except:
    
    try:
        out = content.decode('iso-8859-1')
    except:
        out = content

print ('out', out)
print (type(out))
print (rs.headers)
print (rs.status_code, rs.url)

