# -*- coding: utf-8 -*-
import re
from urllib.request import Request
import requests
from urllib.parse import urlparse, urljoin, unquote
from urllib.request import Request
url = 'http://vnexpress.net/a'
rs = urljoin(url,'.')
print (rs)