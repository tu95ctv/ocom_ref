from odoo import models, fields, api
from odoo import api, fields, models, tools, _, SUPERUSER_ID


class Sale(models.Model):
    # _name = 'ece.ece'
    _inherit = 'sale.order'

    @tools.ormcache('self.id')
    def get_sol_group_by_company(self):
        sol_groups = {}
        for line in self.order_line:
            company_id = line.product_id.company_id
            lines = sol_groups.setdefault(company_id, self.env['sale.order.line'])
            lines |=line
            print ('*lines', lines)
            sol_groups[company_id] = lines

        print ('**sol_groups***', sol_groups)
        return sol_groups


    def tach_don(self):
        lines = self.order_line
        group = {}
        for l in lines: 
            key  = l.product_id.company_id
            d = group.setdefault(key, self.env['sale.order.line'])
            group[key] = d | l

        for c in group:
            print ('company la gi', c)
            line_group = group[c]
            c = c or self.env['res.company'].browse(1)
            warehouse_id = self.with_user(1).with_company(c)._default_warehouse_id()
            order_new = self.with_company(c).copy({'order_line':False, 'company_id':c.id, 'warehouse_id':warehouse_id.id})
            order_line  = [line.with_company(c).copy({'order_id':order_new.id}).id for line in line_group]
            # order_new.order_line = order_line
            
    @api.constrains('company_id', 'sale_order_option_ids')
    def _check_optional_product_company_id(self):
        pass

    @api.constrains('company_id', 'order_line')
    def _check_order_line_company_id(self):
        pass


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_id = fields.Many2one(check_company=False)  # Unrequired company


