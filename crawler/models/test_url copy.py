# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import re
from urllib.request import Request
import requests
from urllib.parse import urlparse, urljoin, unquote
import json
def get_domain(url, remove_www=True, separator='▼▲'):
    parts = url.split(separator)
    url = parts[0]
    ret = urlparse(url).netloc
    if remove_www:
        ret = re.sub(r'www[^.]*.', '', ret)
    return str(ret)
r = '''
lg.jp
or.jp
go.jp
okayama.jp
yamanashi.jp
tokyo.jp
chiba.jp
ibaraki.jp
kanagawa.jp
gunma.jp
toyama.jp
aichi.jp
jp
'''
rs = [i for i in re.split('\s', r) if i ]
print (json.dumps(rs))
def trim_ext(do_d1):
    for i in rs:
        i = '.' + i
        if do_d1.endswith(i):
            do_d1 = do_d1.rsplit(i)[0]
            break
    return do_d1
# https://www2.city.toyohashi.aichi.jp => https://www.city.toyohashi.lg.jp/
# http://www.city.niigata.jp/ => 	http://www.city.niigata.lg.jp/
u1 = 'https://www2.city.toyohashi.aichi.jp'
d1 = 'https://www.city.toyohashi.lg.jp/'

u1 = 'http://www.city.niigata.jp/'
d1 = 'http://www.city.niigata.lg.jp/'

do_u1 = get_domain(u1)
do_d1 = get_domain(d1)

print (trim_ext(do_u1), trim_ext(do_d1))
