import os
import urllib.request
import logging
from hashlib import md5
import re
from urllib.parse import urlparse, urljoin, unquote
import os
import urllib.request
import logging
from hashlib import md5
import re
from urllib.parse import urlparse, urljoin, unquote
# from core.models.targets import Target
import requests
import validators


def get_domain(url, remove_www=True, separator='▼▲'):
    try:
        parts = url.split(separator)
        url = parts[0]
        ret = urlparse(url).netloc
        if remove_www:
            ret = re.sub(r'www[^\.]*.', '', ret)
        return str(ret)
    except Exception as er:
        logging.error(er)
        return None
# import validators
# https://www2.city.toyohashi.aichi.jp => https://www.city.toyohashi.lg.jp/

#
url = 'https://www2.city.toyohashi.aichi.jp'
domain = get_domain(url)
print ('domain', domain)
def get_prefix_middle_postfix(domain):
    #Domain can be www.abc.xyz or abc.xyz
    #Return prefix_origin, mid, postfix_origin
    domain_splits = domain.split('.')
    if len(domain_splits) == 2:
        return '', domain_splits[0], domain_splits[-1]
    elif len(domain_splits) > 2:
        return domain_splits[0], '.'.join(domain_splits[1:-1]), domain_splits[-1]
    else:
        raise ValueError('Domain must has at least 1 dot')