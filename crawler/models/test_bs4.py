# -*- coding: utf-8 -*-
import re
# from urllib.request import urlopen,Request
# import requests
# url = "https://www.pref.aomori.lg.jp/kensei/zaisan/index_1.html"
# url = 'https://ppi.keiyaku.city.hiroshima.lg.jp/PPI_P/'
# headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'} 

# # request=Request(url,None,headers) #The assembled request
# # response = urlopen(request)
# # data = response.read().decode('utf-8') # The data u need
# # print(data)

# rs = requests.get(url, timeout=3, headers=headers)
# content_type = rs.headers.get('Content-Type')
# charset_decode = 'utf-8'
# try:
#     charset = content_type.split(';')[1].split('=')[1]
#     if charset.lower() in ['ms932']:
#         charset_decode = 'shift_jis'
# except:
#     pass
# out = rs.content.decode('shift_jis')
# print ('out', out)
# print (type(out))
# # print (rs.content.decode('utf-8'))
# # print (rs.content.decode('shift_jis'))

# last_part_url = 'a'
# rs = re.search('[\w|\.]+',last_part_url)
# print (rs)
# a = 'alkdfjld.txt'

# rs = re.search('(?<=\.)\w+',a)
# print (rs.group(0))

html_doc= '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html lang="ja" xml:lang="ja" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta http-equiv="Content-Style-Type" content="text/css" />
<meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=yes" />
<meta name="description" content="岩手県議会事務局が管理するホームページ" />
<meta name="keywords" content="岩手県,岩手,いわて,議会" />
<meta name="GENERATOR" content="JustSystems Homepage Builder Version 17.0.15.0 for Windows" />
<title>ホームページリニューアルのお知らせ</title>

<style type="text/css">
<!--
body{
	margin:0px;
	padding:0px;
	font-family:"ヒラギノ角ゴ Pro W3", "Hiragino Kaku Gothic Pro", "メイリオ", Meiryo, Osaka, "ＭＳ Ｐゴシック", "MS PGothic", sans-serif;
	background:#ffffff;
	text-align:center;
}
#wrap{
	width:100%;
	font-size:85%;
}
#pagebody{
	margin:0px auto 0px auto;
	max-width:960px;
	text-align:left;
}
#content2 h1{
	margin-bottom:15px;
	padding:14px 0px 10px 15px;
	font-size:130%;
	font-weight:bold;
	border-bottom:4px solid #08215F;
}
#content2 h2{
	margin-bottom:15px;
	padding:8px 0px 8px 12px;
	font-size:120%;
	border-left:4px solid #DFE0E6;
}
#content2 p{
	padding:0px 15px 15px 15px;
	line-height:1.8;
}
-->
</style>
<meta http-equiv="refresh" content="5;URL=https://www.pref.iwate.jp/gikai/index.html" />
</head>

<body>


<div id="pagebody">
<div id="content2">




<h1>サイトリニューアルのお知らせ</h1>

<p>岩手県議会ホームページは、令和3年2月8日にリニューアルを実施しました。<br />
    サイトリニューアルに伴い、ホームページのアドレス（URL）が変更になりました。<br />
    <br />
    本ＵＲＬからは、約5秒後に変更後の新ＵＲＬへ自動的に転送されますが、<br />
    自動的に転送されない場合につきましては、以下のリンクからお入りください。 </p>

<ul class="objectlink">
<li><a href="https://www.pref.iwate.jp/gikai/index.html">岩手県議会ホームページ </a></li>
    </ul>
    　　【新ＵＲＬ】 https://pref.iwate.jp/gikai/
    <p>お手数をお掛けしますが、お気に入りやブックマークにご登録をいただいている方は、登録の変更をお願いいたします。 </p>
    <br />
    <h2>サイトリニューアルに関する問い合わせ先</h2>
    <p>
岩手県議会事務局 議事調査課<br />
〒020-8570　岩手県盛岡市内丸10番1号<br />
電話（019）629-6020<br />
ファックス（019）629-6014
</p>
    <p>
Copyright © Iwate Prefectural Government All Rights Reserved.
</p>

</div>
</div>

</body>
</html>
'''
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, 'html.parser')
refresh_rs = soup.find_all(attrs={"http-equiv": "refresh"})
rs = [i['content'] for i in refresh_rs]
print (rs)