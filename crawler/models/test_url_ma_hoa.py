# -*- coding: utf-8 -*-
import re
from urllib.request import urlopen,Request
import requests
url = "https://chotatsu2.pref.hiroshima.lg.jp/ebidPPIPublish/EjPPIt"
url = 'https://www.cals.pref.yamanashi.lg.jp/'

# url = 'https://ppi.keiyaku.city.hiroshima.lg.jp/PPI_P/'
headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'} 

# request=Request(url,None,headers) #The assembled request
# response = urlopen(request)
# data = response.read().decode('utf-8') # The data u need
# print(data)

rs = requests.get(url, timeout=3, headers=headers)
content_type = rs.headers.get('Content-Type')
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
    out = rs.content.decode(charset_decode)
except:
    out = rs.content.decode('iso-8859-1')

print ('out', out)
print (type(out))




# print (rs.content.decode('utf-8'))
# print (rs.content.decode('shift_jis'))

# last_part_url = 'a'
# rs = re.search('[\w|\.]+',last_part_url)
# print (rs)
# a = 'alkdfjld.txt'

# rs = re.search('(?<=\.)\w+',a)
# print (rs.group(0))

# html_doc= '''	<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">



# <HTML lang="ja">



# <HEAD>

# 	<META http-equiv="content-type" content="text/html; charset=Shift_JIS">

# 	<TITLE>R§ö¤Æ|[^TCg</TITLE>

# </HEAD>

# <frameset cols="20%,80%" frameborder="0">

# 	<frame src="left.html" noresize>

# 	<frameset rows="93%,7%" frameborder="0">

# 		<frame src="top.html">

# 		<frame src="bottom.html">

# </frameset>

# </HTML>
# '''
# from bs4 import BeautifulSoup
# soup = BeautifulSoup(html_doc, 'html.parser')
# rs = soup.findAll('frame')
# rs = [i['src'] for i in rs]
# print (rs)