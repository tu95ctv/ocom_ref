from odoo import models, fields, api
from odoo import api, fields, models, tools, _, SUPERUSER_ID


class Sale(models.Model):
    # _name = 'ece.ece'
    _inherit = 'sale.order'

    # @tools.ormcache('self.id')
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
            
    # @api.constrains('company_id', 'sale_order_option_ids')
    # def _check_optional_product_company_id(self):
    #     pass

    # @api.constrains('company_id', 'order_line')
    # def _check_order_line_company_id(self):
    #     pass
    
    def _check_carrier_quotation(self, force_carrier_id=None):
        self.ensure_one()
        DeliveryCarrier = self.env['delivery.carrier']

        if self.only_services:
            self.write({'carrier_id': None})
            self._remove_delivery_line()
            return True
        else:
            self = self.with_company(self.company_id)
            # attempt to use partner's preferred carrier
            if not force_carrier_id and self.partner_shipping_id.property_delivery_carrier_id:
                force_carrier_id = self.partner_shipping_id.property_delivery_carrier_id.id

            carrier = force_carrier_id and DeliveryCarrier.browse(force_carrier_id) or self.carrier_id
            available_carriers = self._get_delivery_methods()
            if carrier:
                if carrier not in available_carriers:
                    carrier = DeliveryCarrier
                else:
                    # set the forced carrier at the beginning of the list to be verfied first below
                    available_carriers -= carrier
                    available_carriers = carrier + available_carriers
            if force_carrier_id or not carrier or carrier not in available_carriers:
                for delivery in available_carriers:
                    verified_carrier = delivery._match_address(self.partner_shipping_id)
                    if verified_carrier:
                        carrier = delivery
                        break
                self.write({'carrier_id': carrier.id})
            self._remove_delivery_line()
            if carrier:
                res = carrier.rate_shipment(self)
                if res.get('success'):
                    self.set_delivery_line(carrier, res['price'])
                    self.delivery_rating_success = True
                    self.delivery_message = res['warning_message']
                else:
                    self.set_delivery_line(carrier, 0.0)
                    self.delivery_rating_success = False
                    self.delivery_message = res['error_message']
        return bool(carrier)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_id = fields.Many2one(check_company=False)  # Unrequired company


