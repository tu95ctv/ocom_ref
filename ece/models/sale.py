from odoo import models, fields, api
from odoo import api, fields, models, tools, _, SUPERUSER_ID

class SOL(models.Model):
    _inherit = 'sale.order.line'

    company2_id = fields.Many2one('res.company')

class GR(models.AbstractModel):
    _name = 'ece.gr'
    
    company_id = fields.Many2one('res.company')
    sol_ids = fields.Many2many('sale.order.line')
class Sale(models.Model):
    # _name = 'ece.ece'
    _inherit = 'sale.order'

    sol_gr_ids = fields.Many2many('ece.gr', compute='_compute_sol_gr_ids')

    def _compute_sol_gr_ids(self):
        for r in self:
            sol_groups = r.get_sol_group_by_company()
            ece_gr_ids = self.env['ece.gr']
            for company_id,sols in sol_groups.items():
                gr_obj = self.env['ece.gr'].new({'company_id': company_id,
                     'sol_ids':[(6,0, sols.ids)]})
                ece_gr_ids |=gr_obj
            r.sol_gr_ids = ece_gr_ids


    # @tools.ormcache('self.id')
    def get_sol_group_by_company(self):
        sol_groups = {}
        for line in self.order_line:
            company_id = line.product_id.company_id
            lines = sol_groups.setdefault(company_id, self.env['sale.order.line'])
            lines |=line
            sol_groups[company_id] = lines

        return sol_groups


    def tach_don(self):
        lines = self.order_line
        group = {}
        for l in lines: 
            key  = l.company2_id or l.product_id.company_id
            d = group.setdefault(key, self.env['sale.order.line'])
            group[key] = d | l

        for c in group:
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
    
    def _check_carrier_quotation(self, force_carrier_id=None, company=None):
        # print ('*company in _check_carrier_quotation', company)
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
            self._remove_delivery_line(company)
            # print ('**carrier**', carrier)
            if carrier:
                # print ('đưa context vào company', company)
                res = carrier.with_context(web_company=company).rate_shipment(self, company=company)
                #ĐƯA COMPANY VÀO ĐÂY
                if res.get('success'):
                    self.set_delivery_line(carrier, res['price'],company=company)
                    self.delivery_rating_success = True
                    self.delivery_message = res['warning_message']
                else:
                    self.set_delivery_line(carrier, 0.0)
                    self.delivery_rating_success = False
                    self.delivery_message = res['error_message']
        return bool(carrier), res.get('price', 0.0)
    
    #tham khảo
    # def _remove_delivery_line(self):
    #     self.env['sale.order.line'].search([('order_id', 'in', self.ids), ('is_delivery', '=', True)]).unlink()

    def set_delivery_line(self, carrier, amount, company=None):
        self._remove_delivery_line(company=company)

        for order in self:
            order.carrier_id = carrier.id
            order._create_delivery_line(carrier, amount,company=company)
        return True

    def _remove_delivery_line(self, company=None):
        domain=[('order_id', 'in', self.ids), ('is_delivery', '=', True)]
        if  isinstance(company, int):
            domain.append(('company2_id','=', company))
        self.env['sale.order.line'].search(domain).unlink()

    
    def _create_delivery_line(self, carrier, price_unit, company=None):
        SaleOrderLine = self.env['sale.order.line']
        if self.partner_id:
            # set delivery detail in the customer language
            carrier = carrier.with_context(lang=self.partner_id.lang)

        # Apply fiscal position
        taxes = carrier.product_id.taxes_id.filtered(lambda t: t.company_id.id == self.company_id.id)
        taxes_ids = taxes.ids
        if self.partner_id and self.fiscal_position_id:
            taxes_ids = self.fiscal_position_id.map_tax(taxes, carrier.product_id, self.partner_id).ids

        # Create the sales order line
        carrier_with_partner_lang = carrier.with_context(lang=self.partner_id.lang)
        if carrier_with_partner_lang.product_id.description_sale:
            so_description = '%s: %s' % (carrier_with_partner_lang.name,
                                        carrier_with_partner_lang.product_id.description_sale)
        else:
            so_description = carrier_with_partner_lang.name
        values = {
            'order_id': self.id,
            'name': so_description,
            'product_uom_qty': 1,
            'product_uom': carrier.product_id.uom_id.id,
            'product_id': carrier.product_id.id,
            'tax_id': [(6, 0, taxes_ids)],
            'is_delivery': True,
           
        }
        if  isinstance(company,int):
            values['company_id'] = company

        if carrier.invoice_policy == 'real':
            values['price_unit'] = 0
            values['name'] += _(' (Estimated Cost: %s )', self._format_currency_amount(price_unit))
        else:
            values['price_unit'] = price_unit
        if carrier.free_over and self.currency_id.is_zero(price_unit) :
            values['name'] += '\n' + 'Free Shipping'
        if self.order_line:
            values['sequence'] = self.order_line[-1].sequence + 1
        
        
        if company=='all':
            company_ids = self.sol_gr_ids.company_id
            create_vals = []
            for company in company_ids:
                new_values = values.copy()
                new_values['company2_id'] = company.id
                res = carrier.with_context(web_company=company.id).rate_shipment(self, company=company.id)

                if res.get('success'):
                    price_unit =  res['price']
                else:
                    price_unit =  0.0
                new_values['price_unit'] = price_unit
                create_vals.append(new_values)
        else:
            if isinstance(company,int):
                values['company2_id'] = company

            create_vals = [values]
        sol = SaleOrderLine.sudo().create(create_vals)
        return sol




class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_id = fields.Many2one(check_company=False)  # Unrequired company


