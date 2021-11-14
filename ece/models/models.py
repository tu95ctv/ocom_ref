# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ece(models.Model):
    # _name = 'ece.ece'
    _inherit = 'ir.model.data'

    @api.model
    def set_noupdate_false(self, xml_id):
        id,_,_ = self.xmlid_lookup(xml_id)
        imd = self.browse(id)
        print ('imd', imd)
        imd.noupdate = False

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.constrains('company_id')
    def _check_sale_product_company(self):
        pass

