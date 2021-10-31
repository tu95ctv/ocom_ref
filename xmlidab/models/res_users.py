
from odoo import models, fields, api

class Partner(models.Model):
    _inherit = 'res.partner'

    def name_get(self):
        print ('**name_get**')
        # result = []
        # for so_line in self.sudo():
        #     name = '%s - %s' % (so_line.order_id.name, so_line.name and so_line.name.split('\n')[0] or so_line.product_id.name)
        #     if so_line.order_partner_id.ref:
        #         name = '%s (%s)' % (name, so_line.order_partner_id.ref)
        #     result.append((so_line.id, name))
        rs = super().name_get()
        for ng,r in zip(rs,self):
            name = ng[1]
            name = '%s:%s'%(name,r.email)
            ng[1] = name
        print ('rs name_get', rs)
        return rs
    
    def name_get(self):
        print ('name,get')
        # result = []
        # for so_line in self.sudo():
        #     name = '%s - %s' % (so_line.order_id.name, so_line.name and so_line.name.split('\n')[0] or so_line.product_id.name)
        #     if so_line.order_partner_id.ref:
        #         name = '%s (%s)' % (name, so_line.order_partner_id.ref)
        #     result.append((so_line.id, name))
        # rs = super().name_get()
        rs = []
        for r in self:
            name = '%s:%s'%(r.name,r.email)
            rs.append((r.id, name))
        return rs
