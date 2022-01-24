# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class my_sale(models.Model):
    _name = 'my_sale.order'
    _description = "My Sales Order"

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False, default=fields.Datetime.now, help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.")
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    partner_id = fields.Many2one(
        'res.partner', string='Customer', readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        required=True, change_default=True, index=True, tracking=1,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",)

    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)
    transaction_ids = fields.Many2many('payment.transaction', 'my_sale_order_transaction_rel', 'sale_order_id', 'transaction_id',
                                       string='Transactions', copy=False, readonly=True)

    order_line = fields.One2many('my_sale.order.line', 'order_id')
    amount_total = fields.Float(string='Total', store=True, readonly=True, compute='_amount_all', tracking=4)

    @api.depends('order_line.price_total')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_total = 0.0
            for line in order.order_line:
                amount_total += line.price_total
            order.amount_total = amount_total

class mysaleline(models.Model):
    _name = 'my_sale.order.line'
    _description = "My Sales Order line"

    order_id = fields.Many2one('my_sale.order',required=True, ondelete='cascade')
    order2_id = fields.Many2one('my_sale.order')
    product_id = fields.Many2one('product.product', required=1)
    product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True, default=1.0)
    price_unit = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0)
    price_total = fields.Float(compute='_compute_amount', string='Total', readonly=True, store=True)


    @api.depends('product_uom_qty', 'price_unit')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for record in self:
            record.price_total = record.price_unit * record.product_uom_qty
            

