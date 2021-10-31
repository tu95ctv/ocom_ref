# -*- coding: utf-8 -*-

from odoo import models, fields, api
from lxml import etree
# special columns automatically created by the ORM
LOG_ACCESS_COLUMNS = ['create_uid', 'create_date', 'write_uid', 'write_date']
# MAGIC_COLUMNS = ['id'] + LOG_ACCESS_COLUMNS
from xml.etree.ElementTree import Element, SubElement, tostring, XML

class xmlidab(models.AbstractModel):
    _inherit = 'base'
    # _description = 'xmlidab.xmlidab'

    xmlidab = fields.Char(compute='_compute_xmlidab', search='_search_xmlidab')    

    def get_metadatas(self):
        IrModelData = self.env['ir.model.data'].sudo()
        if self._log_access:
            res = self.sudo().read(LOG_ACCESS_COLUMNS)
        else:
            res = [{'id': x} for x in self.ids]
        xml_data = dict((x['res_id'], x) for x in IrModelData.search_read([('model', '=', self._name),
                                                                           ('res_id', 'in', self.ids)],
                                                                          ['res_id', 'noupdate', 'module', 'name'],
                                                                          order='id'))
        for r in res:
            value = xml_data.get(r['id'], {})
            r['xmlid'] = '%(module)s.%(name)s' % value if value else False
            r['noupdate'] = value.get('noupdate', False)
        print ('**res get_metadatas**', res)
        return res


    # def _compute_xmlidab(self):
    #     if self.ids:
    #         rs = self.get_metadatas()
    #         print ('rs',rs)
    #         for r,v in zip(self,rs):
    #             print (r,v)
    #             if bool(r.id):
    #                 r.xmlidab = v['xmlid']
                
    #     else:
    #         self.xmlidab = False

    def _compute_xmlidab(self):
        if self.ids:
            rs = self.get_metadatas()
            print ('rs',rs)
            for r,v in zip(self,rs):
                print (r,v)
                if isinstance(r.id, models.NewId):
                    r.xmlidab = False
                else:
                    r.xmlidab = v['xmlid']
        else:
            self.xmlidab = False

    def _compute_xmlidab(self):
        self.xmlidab = False

    # def _compute_xmlidab(self):
    #     m = self.get_metadatas()
    #     # for r,v in zip(self,rs):
    #     for c,r in enumerate(self):
    #         r.xmlidab = m[c]['xmlid']
 


    def _search_xmlidab(self, operator, operand):
        if '.' in operand:
            module, name = operand.split('.')
            dm =  [ 
                ('model', '=', self._name),
                ('module', 'ilike', module),
                ('name', 'ilike', name)]
        else:
            dm =  [ 
                ('model', '=', self._name),
                ('name', 'ilike', operand)]
        rs = self.env['ir.model.data'].search(dm, limit=1000)
        rs = rs.mapped('res_id')
        rs = [('id', 'in', rs)]
        return rs



    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super().fields_view_get(view_id, view_type, toolbar=toolbar, submenu=False)
        xpaths_common = ("//page[@string='%(str_page)s']//field",)
        xpaths_basic_info = ("//field",)
        node = Element('<field name="xmlidab" />')
        if view_type in ['tree','search']:#and self._name in ['ir.model.access']:# and res.get('toolbar',False):
            doc = etree.XML(res['arch'])
            # print ('doc',etree.tostring(doc, encoding='unicode'))
            # doc.extend(node)
            # print ('doc2',etree.tostring(doc, encoding='unicode'))
            # res['arch'] = etree.tostring(doc, encoding='unicode')

            ### thử
            view_arch = '''
            <field name="name" position="before">
                    <field name="xmlidab"/>
                </field>
            '''
            arch_tree = etree.fromstring(view_arch.encode('utf-8'))
            # doc = self.env['ir.ui.view'].apply_inheritance_specs(doc, arch_tree)
            for child in arch_tree:
                doc.append(child)

            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res


# class IrModelAccess(models.Model):
#     _name = 'ir.model.access'
#     # _description = 'Model Access'
#     # _order = 'model_id,group_id,name,id'
#     _inherit=['ir.model.access','xmlidab.xmlidab']

    # xmlidab = fields.Char(compute='_compute_xmlidab')    

    # def get_metadatas(self):
    #     IrModelData = self.env['ir.model.data'].sudo()
    #     if self._log_access:
    #         res = self.sudo().read(LOG_ACCESS_COLUMNS)
    #     else:
    #         res = [{'id': x} for x in self.ids]
    #     xml_data = dict((x['res_id'], x) for x in IrModelData.search_read([('model', '=', self._name),
    #                                                                        ('res_id', 'in', self.ids)],
    #                                                                       ['res_id', 'noupdate', 'module', 'name'],
    #                                                                       order='id'))
    #     for r in res:
    #         value = xml_data.get(r['id'], {})
    #         r['xmlid'] = '%(module)s.%(name)s' % value if value else False
    #         r['noupdate'] = value.get('noupdate', False)
    #     return res


    # def _compute_xmlidab(self):
    #     if self.ids:
    #         rs = self.get_metadatas()
    #         print ('rs',rs)
    #         for r,v in zip(self,rs):
    #             print (r,v)
    #             r.xmlidab = v['xmlid']



     
    
