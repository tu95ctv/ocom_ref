from odoo import models,fields, api
from odoo.exceptions import UserError
import requests
from lxml import etree, html
import re
class CPU(models.Model):
    _name = 'bds.cpu'

    name = fields.Char()
    mark = fields.Char()
    rank = fields.Char()
    price = fields.Char()

    cpu_name = fields.Char(compute='_compute_cpu_name_ghz', store=True)
    ghz = fields.Char(compute='_compute_cpu_name_ghz', store=True)


    
    def _get_cpu_name_and_ghz(self, s):
        ghz = None
        last = None
        if s:
            s = s.strip()
            p = '@* *([\d\.\s]+(?:ghz|mhz))$'
            res = re.search(p,s,flags=re.I)
            ghz=None
            
            if res:
                print ('res', res, res.group(0))
                s = re.sub(p,'',s, flags=re.I).strip()
                print ('s', s)
                ghz = res.group(1)
            for i in reversed(s.split()):
                if len(i) > 3:
                    last = i
                    break
            if last:
                last = re.split('-|\s',last)[-1]
        return last, ghz

    @api.depends('name')
    def _compute_cpu_name_ghz(self):
        for r in self:
            r.cpu_name, r.ghz = r._get_cpu_name_and_ghz(r.name)




    def create_or_update(self,keys=[], vals={}):
        domain = []
        for k in keys:
            # v = vals.pop(k)
            v = vals[k]
            domain.append((k,'=',v))
        objs = self.search(domain)
        if len(objs)> 1:
            raise UserError('phát hiện ra có nhiều hơn objects với domain là :%s'%(domain))
        elif len(objs) == 1:
            pass
        else:
            objs = self.create(vals)
        return objs
        
    def parse_cpu_from_html_file(self):
        f=open(r'C:\Users\nguye\Desktop\crawler\1.html','r')
        page_source = f.read()
        f.close()

        def get_node_text(node):
            return ''.join(node.itertext())
        def get_xml_indirect_links(page_source):#New function
                parser = html.HTMLParser(recover=True, encoding='utf-8')
                page_source_etree = etree.fromstring(page_source, parser=parser)
                res = page_source_etree.xpath(".//table[@id='cputable']//tr")
                return res
        rs = get_xml_indirect_links(page_source)

        count =0
        for r1 in rs:
            try:
                xml_tds = r1.xpath('.//td')
                name = get_node_text(xml_tds[0])
                mark = get_node_text(xml_tds[1])
                rank = get_node_text(xml_tds[2])
                price = get_node_text(xml_tds[3])
                self.create_or_update(['name'], {'name':name,'mark':mark,'rank':rank,'price':price})
                count +=1
            except:
                pass





