import os
import urllib.request
import logging
from hashlib import md5
import re
from urllib.parse import urlparse, urljoin, unquote

import validators


def get_domain(url, remove_www=True, separator='▼▲'):
    try:
        parts = url.split(separator)
        url = parts[0]
        ret = urlparse(url).netloc
        if remove_www:
            ret = re.sub(r'www[^.]*.', '', ret)
        return str(ret)
    except Exception as er:
        logging.error(er)
        return None


def get_branch(url, remove_www=True):
    try:
        url = url.strip()
        url = str(urljoin(url, '.')[:-1])
        ret = urlparse(url)
        path = ret.path
        if path.__contains__("/"):
            try:
                parts = ret.path.split("/")
                extensions = os.path.splitext(parts[-1])[1]
                if extensions is not None and extensions != "":
                    path = "/".join(parts[:-1])
            except:
                pass
        netloc = ret.netloc
        if remove_www:
            netloc = str(re.sub(r'www[^.]*.', '', netloc))
        return str(f'{netloc}{path}')
    except Exception as er:
        logging.error(er)
        return None


def get_hashcode(url):
    return md5(url.encode()).hexdigest()


def remove_bookmark(url):
    p = r'#[^\/].*|#$'
    return str(re.sub(p, '', url)).strip()


# https://www.narata.lg.jp/test/index.html
#  domain => [narata.lg.jp]
#  branch => [narata.lg.jp/test/]
def get_scope(url, scope_type='domain'):
    # 1. url mồi => Tìm các url candidates (truy xuất được)
    # 2. Mỗi candidate => scope(candidate)
    # 3. Trả về union(scope i)
    domain = get_domain(url)
    branch = get_branch(url)
    scope = []
    if scope_type == 'domain':
        scope.append(domain)
    else:
        if scope_type == 'branch':
            scope.append(f'{branch}/')
        else:
            scope.append(f'{url}')

    return scope


def is_equal(url1, url2, exact_match=False):
    if exact_match:
        return url1 == url2

    parser1 = urlparse(url1)
    parser2 = urlparse(url2)
    if parser1.scheme != parser2.scheme:
        return False
    elif parser1.netloc != parser2.netloc:
        return False
    elif parser1.port != parser2.port:
        return False
    elif exact_match and parser1.path != parser2.path:
        return False
    elif not exact_match:
        path1 = f"{parser1.path}/".replace("//", "/")
        path2 = f"{parser1.path}/".replace("//", "/")
        if path1 != path2:
            return False
    elif parser1.query != parser2.query or parser1.fragment != parser2.fragment:
        return False

    return True


def in_scope(scope, url, include_subdomain=False):
    if url is None:
        return False

    if scope is None or len(scope) == 0:
        return True

    for item in scope:
        domain = get_domain(url)
        if domain is None:
            return False
        elif domain == item:
            return True
        elif include_subdomain and domain.endswith(item):
            return True
        branch = get_branch(url)
        branch = f'{branch}/'
        # print(branch)
        if branch is not None and branch.startswith(item):
            return True

    return False


def join_link(root_url, href):
    url = unquote(remove_bookmark(href)).strip()
    # @FIXME improve the following code
    if url.startswith('javascript:') \
            or url.endswith(".css") \
            or url.endswith(".jpg") or url.endswith(".jpeg") or url.endswith(".png") or url.endswith(
        ".gif") or url.endswith(".ico") \
            or url.endswith(".mov") or url.endswith(".mp4") or url.endswith(".mp3") \
            or url.endswith('.js'):
        return None

    url = re.sub(r"(\n)+", "", url)
    if not (url[0:7] == 'http://' or url[0:8] == 'https://'):
        url = urljoin(root_url, url)

    url = unquote(remove_bookmark(url)).strip()
    url = re.sub(r"(\n)+", "", url)
    valid = validators.url(url)
    return url if valid else None
