import os
import urllib.request
import logging
from hashlib import md5
import re
from urllib.parse import urlparse, urljoin, unquote

# import validators


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


def get_branch(url):
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
        return str(f'{ret.netloc}{path}')
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

# url = 'https://vnexpress.netx/abc/def'
# # rs = get_branch(url)
# # rs =get_scope(url)
# # print (rs)
# # rs = urljoin(url, '.')
# ret = urlparse(url)
# netloc=ret.netloc

# print ('netloc', netloc)

# os.path.splitext(netloc)

def find_candidate(url):
    candidates = set()
    schemes = ['http', 'https']
    prefixes = ['www.']
    postfixes = ['.lg.jp']
    parser = urllib.parse.urlparse(url)
    for scheme in schemes:
        candidates.add(f"{scheme}://{parser.netloc}{parser.path}")

        for prefix in prefixes:
            if not parser.netloc.startswith(prefix):
                candidates.add(f"{scheme}://{prefix}{parser.netloc}{parser.path}")
            for postfix in postfixes:
                if not parser.netloc.endswith(postfix):
                    candidates.add(f"{scheme}://{parser.netloc[:-3]}{postfix}{parser.path}")
                    candidates.add(f"{scheme}://{prefix}{parser.netloc[:-3]}{postfix}{parser.path}")

    # --------------
    ret = set()
    for candidate_url in candidates:
        if candidate_url != url and is_avaible(candidate_url):
            check = Target.find_by_url(candidate_url)
            if check is None:
                ret.add(candidate_url)

    return ret

def get_scheme_domain_path(url):
    scheme, url_exclude_scheme = url.split('//')
    scheme = scheme.replace(':', '')
    url_exclude_scheme_splits = url_exclude_scheme.split('/',1)
    domain = url_exclude_scheme_splits[0]
    if len(url_exclude_scheme_splits) ==1:
        path = None
    else:
        path = url_exclude_scheme_splits[1]
    return scheme, domain, path

def get_prefix_middle_postfix(domain):
    #Domain can be www.abc.xyz or abc.xyz
    #Return prefix_origin, mid, postfix_origin
    domain_splits = domain.split('.')
    if len(domain_splits) == 2:
        return '', domain_splits[0], domain_splits[-1]
    elif len(domain_splits) > 2:
        return domain_splits[0], '.'.join(domain_splits[1:-1]), domain_splits[-1]
    else:
        raise ValueError('domain must has at least 1 dot')


def find_candidates(url, schemes=[], prefixes=[], postfixes=[]):
    scheme_origin, domain, path = get_scheme_domain_path(url)
    prefix_origin, mid, postfix_origin = get_prefix_middle_postfix(domain)
    schemes_plus = {scheme_origin} | set(schemes)
    prefixes_plus = set(map(lambda pre: pre if pre =='' else pre + '.', {prefix_origin} | set(prefixes)))
    postfixes_plus = {postfix_origin} | set(postfixes)
    candidates = []
    path = '' if path == None else '/' + path 
    for sche in schemes_plus:
        for pre in prefixes_plus:
            for pos in postfixes_plus:
                candidates.append(f'{sche}://{pre}{mid}.{pos}{path}')
    return candidates
    # --------------
    # ret = set()
    # for candidate_url in candidates:
    #     if candidate_url != url and is_avaible(candidate_url):
    #         check = Target.find_by_url(candidate_url)
    #         if check is None:
    #             ret.add(candidate_url)
    # return ret

url = 'http://www.vnexpress.net/a/b.html?x=y#k=m&z=l'
# rs = find_candidates(url, schemes=['https','http'], prefixes=['abc','www1'], postfixes=['jg.jp','net'])
# rs = find_candidates(url, schemes=['https','http'], prefixes=['abc','www1'], postfixes=['jg.jp','net'])
# rs = find_candidates(url)
# rs = find_candidates(url)

# print (rs, len(rs),len(set(rs)))

def get_scope(url, scope_type='domain'):
    # 1. url mồi => Tìm các url candidates (truy xuất được)
    # 2. Mỗi candidate => scope(candidate)
    # 3. Trả về union(scope i)
    domain = get_domain(url)
    print ('domain', domain)
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

def get_scopes(url, scope_type='domain', schemes=[], prefixes=[], postfixes=[]):
    candidate_urls = find_candidates(url,schemes, prefixes, postfixes)
    scope_res = set()
    for candidate_url in candidate_urls:
        scopes = get_scope(candidate_url, scope_type)
        scope_res.update(scopes)
    return scope_res
    


rs = get_scopes(url,'url',  schemes=['https','http'], prefixes=['abc','www1'], postfixes=['jg.jp','net'])
print (rs, len(rs), len(set(rs)))


url = 'http://vnexpress.net/a/a.b'
rs = get_scopes(url,'domain', ['https'],['abc'],['vn'])
print (rs.status_code)