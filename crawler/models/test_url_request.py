# -*- coding: utf-8 -*-
import re
from urllib.request import urlopen,Request
import requests
url = "https://www.pref.aomori.lg.jp/kensei/zaisan/index_1.html"
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
    if charset.lower() in ['ms932']:
        charset_decode = 'shift_jis'
except:
    pass
out = rs.content.decode(charset_decode)
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