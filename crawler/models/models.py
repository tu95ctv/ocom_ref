# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
from bs4 import BeautifulSoup
import re
from ast import literal_eval
import traceback
import logging
from lxml import etree, html
from odoo.addons.crawler.models.link_helpers import get_branch as get_branch1
import validators

# from .. import default_headers #điều tra lỗi giùm
from urllib.parse import urlparse, urljoin, unquote
FORCE_add_headers_host = False
FORCE_default_headers = False
default_headers1  = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
        }

default_headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'} 

def remove_bookmark(url):
    p = r'#[^\/].*|#$'
    return str(re.sub(p, '', url)).strip()

def decode_dot_dot(ur, lu):
    ur = re.sub('/$','',ur)
    urs = ur.split('/')
    lus = lu.split('/')
    out_lus = urs[:]
    for i in lus:
        if i == '..':
            out_lus = out_lus[:-1]
        else:
            out_lus.append(i)
    out_lu = '/'.join(out_lus)
    return out_lu

def get_branch(url):
    try:
        url = url.strip()
        url = str(urljoin(url, '.')[:-1])
        print ('*url*', url)
        ret = urlparse(url)
        print ('ret', ret)
        path = ret.path
        if path.__contains__("/"):
            try:
                parts = ret.path.split("/")
                extensions = os.path.splitext(parts[-1])[1]
                print ('*extensions*', extensions)
                if extensions is not None and extensions != "":
                    path = "/".join(parts[:-1])
            except:
                pass
        
        return str(f'{ret.scheme}://{ret.netloc}{path}')
    except Exception as er:
        logging.error(er)
        return None

def cal_domain(url):
    if not re.match('https://|http://', url):
        raise ValueError('must http, https://')
    rus = url.split('//',1) 
    rus1s = rus[1].split('/')
    domain_no_http = rus1s[0]
    domain_has_http = rus[0] + '//' + domain_no_http
    return domain_has_http 

def cal_protocol(ru):
    if not re.match('https://|http://', ru):
        raise ValueError('must http, https://')
    return ru.split('//') [0]

def end_slash_url(ur):
    if not ur.endswith('/'):
        ur = ur + '/'
    return ur

def absolute_ur (re_url, lu):
    lu = remove_bookmark(lu)
    re_url = end_slash_url(re_url)
    if lu.startswith('..'):
        rs =  decode_dot_dot(re_url, lu)
    elif lu.startswith('//'):
        rs = cal_protocol(re_url) + lu
    elif lu.startswith('/') :
        rs = cal_domain(re_url) + lu
    elif  re.search('^\w', lu) and not re.match('https://|http://', lu):
        rs = re_url + lu
    elif not re.search('\w',lu):# không thấy ký tự word nào trong link tìm kiếm
        rs = re_url
    else:
        rs = lu
    return rs

def get_domain(url, remove_www=True, separator='▼▲'):
    parts = url.split(separator)
    url = parts[0]
    ret = urlparse(url).netloc
    if remove_www:
        ret = re.sub(r'www[^.]*.', '', ret)
    return str(ret)

def get_scheme_domain_path(url):
    try:
        scheme, url_exclude_scheme = url.split('//',1)
    except:
        scheme, url_exclude_scheme = '', url
    scheme = scheme.replace(':', '')
    url_exclude_scheme_splits = url_exclude_scheme.split('/',1)
    domain = url_exclude_scheme_splits[0]
    if len(url_exclude_scheme_splits) == 1:
        path = None
    else:
        path = '/' + url_exclude_scheme_splits[1]
    return scheme, domain, path

class crawler(models.Model):
    _name = 'crawler.item'
    _description = 'crawler.item'
    

    crawler_id = fields.Many2one('crawler.crawler', ondelete='cascade')
    url = fields.Char(required=True)
    ab_url = fields.Char()
    title = fields.Char()
    is_match = fields.Boolean()
    phase = fields.Char(related='crawler_id.phase')

    def get_or_create(self, crawler_id=None, url=None, title=None, is_match=None,ab_url=None):
        items = self.search([('crawler_id','=',crawler_id),('ab_url','=',ab_url)])
        if not items:
            self.create({'crawler_id':crawler_id, 'url':url, 'title':title, 'is_match':is_match, 'ab_url':ab_url})
        elif is_match:
            items.is_match = is_match

class crawler(models.Model):
    _name = 'crawler.crawler'
    _description = 'crawler.crawler'
    _order = 'stt'
    _rec_name = 'url'
    url = fields.Char()
    total_links = fields.Integer()
    stt = fields.Integer()
    find_total_links = fields.Integer(default=0, string="Số link tìm thấy")
    time_out = fields.Boolean()
    is_ran = fields.Boolean()
    item_ids = fields.One2many('crawler.item', 'crawler_id')
    match_item_ids = fields.One2many('crawler.item', 'crawler_id', domain=[('is_match','=',True)])
    fail_log = fields.Char()
    processing = fields.Integer()
    success = fields.Integer()
    fails = fields.Integer()
    canceled = fields.Integer()
    content = fields.Html()
    content2 = fields.Text(compute='_compute_content2')
    headers = fields.Text(default=default_headers, requried=True)
    my_note =fields.Text()
    protocol = fields.Char(compute="_compute_re_url", store=True)
    ext = fields.Char(compute="_compute_re_url", store=True)
    domain = fields.Char(compute="_compute_re_url", store=True)
   
    size_content = fields.Integer('độ dài dữ liệu truy xuất') #'<doc></doc>'
    has_dot_last_part_url = fields.Char(compute="_compute_re_url", store=True, string="Đuôi")
    re_url = fields.Char(compute="_compute_re_url", store=True)
    url_ex_http = fields.Char(compute="_compute_re_url", store=True)
    trigger = fields.Boolean()
    len_links = fields.Integer()
    is_favorite = fields.Boolean()
    note = fields.Char('Nhận xét số lượng link')
    nhan_xet = fields.Char(compute='_compute_nhan_xet', store=True, string="Nhận xét SL link")
    dieu_tra = fields.Char(compute='_compute_dieu_tra', store=True, string="Điều tra")
    header_for_parse = fields.Text()
    default_headers = fields.Text(default=default_headers)
    exclude_header_keys = fields.Text()
    is_add_headers_host = fields.Boolean()
    charset = fields.Char()
    content3 = fields.Text()
    show_content3 = fields.Boolean()
    len_frame = fields.Integer(compute='_compute_key_frame', store=True)
    src_frame = fields.Char(compute='_compute_key_frame', store=True)
    redirect = fields.Char(compute='_compute_key_frame', store=True)
    charset_input = fields.Selection([('ms932','ms932'),('windows-31j','windows-31j'),('shift_jis','shift_jis'),('iso-8859-1','iso-8859-1')])
    sumary = fields.Char(compute='_compute_sumary', store=True, string="Trạng thái lỗi")
    giai_phap = fields.Char(compute='_compute_sumary', store=True, string="Cách Fix (nếu có)")
    fix_note = fields.Char()
    phase = fields.Char()
    error_code = fields.Char(compute='_compute_key_frame', store=True)
    prefix = fields.Char(compute='_compute_re_url', store=True)
    load_headers = fields.Char(compute='_onchange_load_header')
    use_headers = fields.Selection([('0','Not Use'),('1','Use Default (Tuấn)'),('2','Use field header'),('3','Use Default 1 (a Đức)')], default='3',)
    response_header = fields.Text()
    response_url = fields.Char()
    domain_has_www = fields.Char()
    first = fields.Char(compute='_compute_re_url', store=True)
    last = fields.Char(compute='_compute_re_url', store=True)
    last_double = fields.Char(compute='_compute_re_url', store=True)
    domain_len = fields.Integer(compute='_compute_re_url', store=True)
    max_domain_part = fields.Char(compute='_compute_re_url', store=True)
    path = fields.Char(compute='_compute_re_url', store=True)
    my_way_path = fields.Char(compute='_compute_re_url', store=True)

    branch = fields.Char(compute='_compute_re_url', store=True)
    my_way_branch = fields.Char(compute='_compute_re_url', store=True)

    is_same_branch = fields.Boolean(compute='_compute_re_url', store=True)

    scrawl_script = fields.Text(compute='_compute_scrawl_script', readonly=False)
    scrawl_script2 = fields.Text(compute='_compute_scrawl_script', readonly=False)
    is_same_url = fields.Boolean(compute='_compute_is_same_url', store=True)
    sql = fields.Text(compute='_compute_sql')
    note_rescan_iframe = fields.Char(compute='_compute_note_rescan_iframe', store=True)
    respone_status_code = fields.Char()
    app = fields.Boolean(compute='_compute_app', store=True)
    is_frame = fields.Boolean(compute='_compute_app', store=True)
    is_form = fields.Boolean(compute='_compute_app', store=True)
    structure_specs = fields.Char(compute='_compute_app', store=True)
    charset_decode = fields.Char(compute='_compute_charset_decode', store=True, readonly=False)
    fault_note  = fields.Text()
    branch1 = fields.Char(compute='_compute_re_url', store=True)
    note1 = fields.Text()
    note2 = fields.Text()
    note3 = fields.Text()

    @api.depends('url','trigger')
    def _compute_re_url(self):
        for r in self:
            protocol = False
            re_url = False
            has_dot_last_part_url = False
            url_ex_http = False
            ext = False
            domain = False
            domain_has_www = False
            first = False
            last = False
            domain_len = False
            last_double = False
            max_domain_part = False
            my_path = False
            path = False
            branch = False
            my_way_path = False
            branch1 = False
            if  r.url:
                url = r.url
                urls = url.split('/')
                if not urls[-1]:
                    urls = urls[:-1] # bỏ / sau url
                protocol, url_ex_http = url.split('//',1)
                
                
                url_ex_https = [i for i in url_ex_http.split('/') if i]
                
                domain = get_domain(url)
                domain_has_www = get_domain(url, False)
                domain_has_www_split_slashs = domain_has_www.split('.')
                domain_has_www_split_slashs_lens = [len(i) for i in domain_has_www_split_slashs]
                max_domain_part_len = max(domain_has_www_split_slashs_lens)
                index_max_domain_part =  domain_has_www_split_slashs_lens.index(max_domain_part_len)
                max_domain_part = domain_has_www_split_slashs[index_max_domain_part]
                domain_len = len(domain_has_www_split_slashs)
                first = domain_has_www_split_slashs[0]
                last = domain_has_www_split_slashs[-1]
                last_double = '.'.join(domain_has_www_split_slashs[-2:])
                re_url=url
                has_dot_last_part_url = False
                ext = False
                if len(url_ex_https)> 1:
                    last_part_url = url_ex_https[-1]
                    is_dot_in_last_part_url = '.' in last_part_url
                    if is_dot_in_last_part_url:
                        re_url = '/'.join(urls[:-1]) +'/'
                        has_dot_last_part_url = last_part_url
                        ext_rs = re.search('(?<=\.)\w+', last_part_url)# search để tim ext
                        ext = ext_rs.group(0)

                    else:
                        has_dot_last_part_url = False
                        re_url = url
                path = urlparse(url).path
                scheme, my_domain, my_way_path = get_scheme_domain_path(url)
                branch = get_branch(url)
                branch1 = get_branch1(url)
            r.branch1 = branch1
            r.my_way_branch = re_url
            r.branch = branch
            r.is_same_branch = branch == re_url
            r.path = path
            r.my_way_path = my_way_path
            r.max_domain_part = max_domain_part
            r.domain_len = domain_len         
            r.first = first
            r.domain_has_www = domain_has_www
            r.first = first
            r.last = last
            r.last_double = last_double
            r.protocol = protocol
            r.re_url = re_url
            r.has_dot_last_part_url = has_dot_last_part_url
            r.url_ex_http = url_ex_http
            r.ext = ext
            r.domain = domain




    @api.depends('charset')
    def _compute_charset_decode(self):
        for r in self:
            charset_decode = 'utf-8'
            charset= r.charset
            if charset:
                if r.charset in ['ms932','windows-31j']:
                    charset_decode = 'shift_jis'
                else:
                    charset_decode = charset
            r.charset_decode = charset_decode

    @api.depends('content3','trigger', 'charset_decode','len_frame')
    def _compute_app(self):
        for r in self:
            print ('rrr')
            app = False
            is_form = False
            is_frame = False
            sums = []
            if r.content3:
                x = None
                try:
                    charset_decode = r.charset_decode
                    parser = html.HTMLParser(recover=True, encoding=charset_decode)
                    x = etree.fromstring(r.content3, parser=parser)
                except:
                    try:
                        # parser = html.HTMLParser(recover=True)
                        # x = etree.fromstring(r.content3)
                        x = etree.XML(r.content3)
                    except:
                        print ('có lỗi khi compute stureture apps', traceback.format_exc())
                        pass
                        app = 'onclick' in r.content3
                        is_frame = r.len_frame
                if x:
                    app = x.xpath("//*[@onclick]")
                    is_form = x.xpath("//form")
                    is_frame = x.xpath("//*[self::iframe or self::frame]") 
                
                print ('**is_frame**', is_frame)
                if app:
                    sums.append('APP')
                if is_form:
                    sums.append('FORM')
                if is_frame:
                    sums.append('FRAME')

                
            r.structure_specs = ','.join(sums)
            r.app = app
            r.is_form = is_form
            r.is_frame = is_frame 

    @api.depends('my_note', 'is_same_url', 'trigger')
    def _compute_note_rescan_iframe(self):
        for r in self:
            if r.my_note:
                rs = r.my_note
            elif not r.is_same_url:
                rs = f"Link response '{r.response_url}' khác với link trong scope '{r.url}'"
            else:
                rs = False
            r.note_rescan_iframe = rs

    def _compute_sql(self):
        for r in self:
            domain = r.domain
            re_url = r.re_url
            re_url = re_url.split('//',1)[1]
            r.sql = f"""
            SELECT * FROM `webdocs` WHERE url LIKE '%{re_url}%'\n
            select * from  webdoc_contents where web_doc_id in (SELECT id FROM `webdocs` WHERE url LIKE  '%{re_url}%')\n
            SELECT * FROM `webdocs` WHERE url LIKE '%{domain}%'\n
            select * from  webdoc_contents where web_doc_id in (SELECT id FROM `webdocs` WHERE url LIKE  '%{domain}%')
            """

    @api.depends('url')
    def _compute_scrawl_script(self):
        for r in self:
            url = r.url
            rs = f'''
    python3 scripts/crawl.py {url}  -s branch \n
    python3 scripts/crawl.py {url} -m=resume -s=domain -f \n
    python3 scripts/rescan_iframes.py {url}  -s branch \n
    python3 scripts/rescan_iframes.py {url} -m=resume -s=domain -f \n
    python3 scripts/rescan_app.py {url}  -s branch \n
    python3 scripts/rescan_app.py {url} -m=resume -s=domain -f\n
            '''
            
            rs2 = re.sub('python3','python',rs)
            r.scrawl_script = rs
            r.scrawl_script2 = rs2

    @api.depends('use_headers', 'exclude_header_keys')
    def _onchange_load_header(self):
        print ('*_onchange_load_header*')
        if FORCE_default_headers:
            headers = default_headers
        elif self.use_headers == '0' or not self.use_headers:
            headers= None
            print ("self.use_headers == '0':")
        elif self.use_headers == '1':
            headers = default_headers
        elif self.use_headers == '3':
            headers = default_headers1
        else:
            headers = self.headers
            if headers:
                headers = literal_eval(headers)
            else:
                if headers == False:
                    headers = None
                else:
                    headers = {}
        print ('**headers**', headers)
        headers = self.exclude_headers(headers) if headers else headers
        print ('**headers2**', headers)
        self.load_headers = headers


    type = fields.Selection([
        ('select','select'),
        ('js','js'),
        ('app','app'),
        ('frame','frame'),
        ('short','short'),
        ('no_reach','403 Forbiden'),
        ('direct','direct'),
        ])
    auto_type = fields.Selection([
        ('select','select'),
        ('js','js'),
        ('app','app'),
        ('frame','frame'),
        ('short','short'),
        ('no_reach','403'),
        ('direct','direct'),
        ],compute='_compute_key_frame', store=True)


    @api.depends('trigger','my_note','fix_note','redirect','len_frame','error_code','auto_type')
    def _compute_sumary(self):
        for r in self:
            if r.len_frame:
                sumary = 'Frame'
                giai_phap = 'Crawl các src của các frame'
            elif r.redirect:
                sumary = 'Redirect'
                giai_phap = 'Crawl redirect link'
            elif r.auto_type:
                # sumary = dict(self._fields['auto_type']._description_selection(self.env))[r.auto_type]
                if r.auto_type == 'no_reach':
                    sumary = r.error_code
                    giai_phap = 'Không cần fix'
            elif r.time_out:
                sumary = 'Không truy xuất được'
                giai_phap = 'Không cần fix'
            else:
                sumary = r.my_note
                giai_phap = r.fix_note
            r.sumary = sumary
            r.giai_phap = giai_phap
    
    
    @api.depends('content')
    def _compute_content2(self):
        for r in self:
            r.content2 = r.content

    @api.depends('content3','trigger')
    def _compute_key_frame(self):
        for r in self:
            len_frame = False
            redirect = False
            src_frame = False
            auto_type = False
            error_code = False
            if r.content3:
                soup = BeautifulSoup(r.content3, 'html.parser')
                rs = soup.findAll('frame')
                len_frame = len(rs)
                try:
                    src_frame = [i['src'] for i in rs]
                except:
                    src_frame = []
                rs = soup.findAll('iframe')
                len_iframe = len(rs)
                len_frame +=len_iframe
                try:
                    src_iframe = [i['src'] for i in rs]
                except:
                    src_iframe = []
                src_frame.extend(src_iframe)
                src_frame = ','.join(src_frame)
                len_frame = len_frame
                ###

                refresh_rs = soup.find_all(attrs={"http-equiv": "refresh"})
                if not refresh_rs:
                    refresh_rs = soup.find_all(attrs={"http-equiv": "Refresh"})
                rs = [i['content'] for i in refresh_rs]
                rs = ','.join(rs)
                if rs:
                    redirect = rs
                else:
                    redirect = False

                #####

                # rs = re.search(r'<title>403 Forbidden</title>', r.content3, flags=re.I)
                rs = re.search(r'<\w{1,10}>\s*(403|404|503).*</\w{1,10}>', r.content3, flags=re.I)
                if rs:
                    auto_type = 'no_reach'
                    error_code = rs.group(1)
            r.error_code = error_code
            r.auto_type = auto_type
            r.len_frame = len_frame
            r.redirect = redirect
            r.src_frame = src_frame

    def exclude_headers(self, headers):
        exclude_header_keys = literal_eval(self.exclude_header_keys) if self.exclude_header_keys else []
        exclude_header_keys = [i.lower() for i in exclude_header_keys]
        headers = {k:v for k,v in headers.items() if k not in exclude_header_keys}
        return headers

    def add_headers_host(self, headers):
        # exclude_header_keys = literal_eval(self.exclude_header_keys) if self.exclude_header_keys else []
        # exclude_header_keys = [i.lower() for i in exclude_header_keys]
        # headers = {k:v for k,v in headers.items() if k not in exclude_header_keys}
        if not headers:
            headers = {}
        headers.update({'host':self.re_url})
        return headers


    @api.onchange('header_for_parse','exclude_header_keys')
    def _onchange_header_for_parse(self):
        sfp = self.header_for_parse
        if sfp:
            # headers  = ( i.split(':',1) for i in sfp.split('\n') if ':' in i)
            headers  = ( i.split(':',1) for i in re.split(r'\r\n|\n', sfp) if ':' in i)
            print ('type(headers)',type(headers))
            headers = {k.lower():re.sub('^\s+','',v) for k,v in headers}
            headers = self.exclude_headers(headers)
            self.headers = headers
        else:
            self.headers = False




    @api.depends('time_out')
    def _compute_dieu_tra(self):
        for r in self:
            rs = 'Không truy xuất được' if r.time_out else 'Truy xuất được'
            r.dieu_tra = rs

    
    @api.depends('total_links','find_total_links','trigger')
    def _compute_nhan_xet(self):
        for r in self:
            tl = r.total_links
            ftl = r.find_total_links
            if ftl == 0:
                rs = 'Không có link'
                if tl < 2:
                    rs += ' (tương đương)'
            else:
                delta = ftl - tl
                abs_delta = abs(delta)
                if ftl == 0:
                    mau_ftl = 1
                else:
                    mau_ftl = ftl
                ti_le = delta/mau_ftl
                abs_ti_le = abs(ti_le)
                if abs_ti_le < 0.3 or abs_delta < 2:
                    rs = 'Tương đương'
                elif delta < 0:
                    rs = 'Ít link hơn'
                else:
                    rs = 'Nhiều link hơn'
            r.nhan_xet = rs

    def clear_item_ids(self):
        self.item_ids = False
        self.find_total_links = False
        self.content=False
        self.len_links=False
        self.content3=False
        self.size_content=False

    def is_match(self, look_url,ab_lu, out=[]):
        rs = False
        ur = self.re_url
        try:
            rs =  self._is_match(ur, look_url, ab_lu)
            if rs:
                out.append(look_url)
        except Exception as e:
            self.fail_log = str(e)
        return rs

    def _is_match(self, ur, look_url, ab_lu):
        if not look_url:
            return False
        if look_url.startswith('#'):
            return False
        if not re.search('\w',look_url): # nếu không có chữ nào thì trả về không match
            return False
        # look_url_ex_http = look_url.split('//')[-1]
        re_url = self.re_url
        rs = re.search('mailto:|javascript:|telephone:|telecom:|tele:|telel:', ab_lu, flags=re.I)
        if rs:
            return False
        rs = re.match(re_url, ab_lu)
        return rs

    @staticmethod  
    def exclude_http(url):
        return url.split('//',1)[1]

    @api.depends('response_url','url', 'trigger')
    def _compute_is_same_url(self):
        for r in self:
            if r.response_url and r.url:
                d1 = get_domain(r.response_url)
                is_same_url = self.exclude_http(r.response_url) == self.exclude_http(r.url)
            else:
                is_same_url = True
            r.is_same_url = is_same_url

    def count_link(self):#ch
        print ('count_link')
        self.clear_item_ids()
        url = self.url
        charset_decode = False
        if FORCE_default_headers:
            headers = default_headers
        elif self.use_headers == '0' or not self.use_headers:
            headers= None
            print ("self.use_headers == '0':")
        elif self.use_headers == '1':
            headers = default_headers
        elif self.use_headers == '3':
            headers = default_headers1
        else:
            headers = self.headers
            if headers:
                headers = literal_eval(headers)
            else:
                if headers == False:
                    headers = None
                else:
                    headers = {}

        headers = self.exclude_headers(headers) if headers else headers
        if self.is_add_headers_host or FORCE_add_headers_host:
            headers = self.add_headers_host(headers)
        try:
            print ('headers',headers)
            print (type(headers))
            rs = requests.get(url, timeout=3, headers=headers, verify=False)
            self.response_header = rs.headers
            self.response_url = rs.url
           
        except Exception as e:
            print ('lỗi: %s '%e)
            # self.respone_status_code = rs.status_code
            if not self.is_ran:
                self.time_out = True
            self.fail_log = str(e)
            print ('lỗi được traceback',traceback.format_exc())
        else:
            self.respone_status_code = rs.status_code
            content_type = rs.headers.get('Content-Type')
            charset_decode = 'utf-8'
            try:
                charset = content_type.split(';')[1].split('=')[1]
                charset = charset.lower()
                self.charset= charset
                if charset in ['ms932','windows-31j']:
                    charset_decode = 'shift_jis'
                else:
                    charset_decode = charset
                
            except:
                pass
            charset_decode = self.charset_input or charset_decode
            self.fail_log = False
            if self.ext not in ['pdf','xls','xlsx']:
                try:
                    html_doc = rs.content.decode(charset_decode)
                except:
                    try:
                        html_doc = rs.content.decode('shift_jis')
                    except:
                        html_doc = rs.content
                        can_not_decode = True
                        charset_decode = False
                        # html_doc = 'can not decode'

                print ('đã request được', html_doc)
                self.content = html_doc
                self.content3 = html_doc
                try:
                    self.flush()
                except:
                    html_doc = 'cant not write'
                    self.content3 = html_doc
                self.size_content = len(html_doc)
                # print ('self.size_content', self.size_content)
                # print ('html_doc', html_doc)
                soup = BeautifulSoup(html_doc, 'html.parser')
                ls = soup.find_all('a')
                out = [self.url]
                self.time_out = False
                ncount = 0
                self.len_links = len(ls)
                for i in ls:
                    lu = i.get('href','')
                    lu = remove_bookmark(lu)
                    crawler_id = self.id
                    title = i.text
                    match = False
                    ab_url = absolute_ur(self.re_url, lu)
                    valid = validators.url(ab_url)
                    print ('**valid**', valid)

                    if lu.startswith('javascript:') \
                            or url.endswith(".css") \
                            or url.endswith(".jpg") or url.endswith(".jpeg") or url.endswith(".png") or url.endswith(
                        ".gif") or url.endswith(".ico") \
                            or url.endswith(".mov") or url.endswith(".mp4") or url.endswith(".mp3") \
                            or url.endswith('.js'):
                        continue
                    if not valid:
                        print ('not valid')
                        continue
                    if lu and ab_url not in out and self.is_match(lu,ab_url,out):
                        ncount +=1
                        match = True
                    self.env['crawler.item'].get_or_create(crawler_id, lu, title, match, ab_url)
                self.find_total_links = ncount
                        
        self.charset_decode = charset_decode
        self.is_ran = True
        self._cr.commit()

