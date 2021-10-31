# import os
# import urllib.request
# import logging
# from hashlib import md5
# import re
# from urllib.parse import urlparse, urljoin, unquote
import validators

# url = 'http://vnexpress.net'
# rs = urlparse(url)
# print (rs)

# try:
#     1/0
# except:
#     print ('abc')
#     raise

url = 'https://www.pref.yamaguchi.lg.jp/cms/a11000/index/javascript:void(0);'
print (validators.url(url))