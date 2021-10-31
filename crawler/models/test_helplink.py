# -*- coding: utf-8 -*-
import re
from urllib.parse import urlparse, urljoin, unquote
url= 'https://sv101.city.toyama.toyama.jp/www/index.html'
src= '//www.pref.yamaguchi.lg.jp/business/'
src = '#ab'
# src = '/abc'
# src = "javascript:open1('http://www.city.toyama.toyama.jp/zaimubu/keiyakuka/denshinyusatsuquestion.html')"
action_url = urljoin(url, src)
print (action_url)
