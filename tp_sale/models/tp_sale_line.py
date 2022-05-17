from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleLine2(models.Model):
    _name = 'tp.sale.order.line2'
    _description = 'TP sale Line 2'

    line2_id = fields.Many2one('tp.sale.order.line1')
    name = fields.Char()
    product_id = fields.Many2one('product.product')


class SaleLine1(models.Model):
    _name = 'tp.sale.order.line1'
    _description = 'TP sale Line 1'

    line1_id = fields.Many2one('tp.sale.order.line1')
    # line2_id = fields.Many2one('tp.sale.order.line1')
    name = fields.Char()
    product_id = fields.Many2one('product.product')
    # line2_ids = fields.Many2many('tp.sale.order.line1','line1_line2_rel','line1_id','line2_id')
    line2_ids = fields.One2many('tp.sale.order.line2','line2_id')

class SaleLine(models.Model):
    _name = 'tp.sale.order.line'
    _description = 'TP sale'


    active = fields.Boolean(default=True)
    product_id = fields.Many2one('product.product', auto_join=1)
    qty = fields.Integer()
    price_unit = fields.Float(digits=(6,2))
    # price = fields.Float(compute='_compute_price', store=True)
    price = fields.Float()
    order_id = fields.Many2one('tp.sale.order', ondelete='cascade')
    dup_order_id = fields.Many2one('tp.sale.order', ondelete='cascade', compute='_compute_dup_order_id', store=True)
    name = fields.Char()
    sale_ids = fields.Many2many('tp.sale.order','so_sol_rel','sol_id','so_id')
    # line1_ids = fields.Many2many('tp.sale.order.line1')
    line1_ids = fields.Many2many('tp.sale.order.line1','line1_id')
    @api.depends('order_id')
    def _compute_dup_order_id(self):
        for r in self:
            r.dup_order_id = r.order_id
            
    # @api.depends('qty', 'price_unit')
    # def _compute_price(self):
    #     for record in self:
    #         record.price = record.qty * record.price_unit

    res_model = fields.Char()
    res_id = fields.Many2oneReference( index=True, model_field='res_model')
    # res_name = fields.Char(
    #     'Document Name', compute='_compute_res_name', compute_sudo=True, store=True,
    #     help="Display name of the related document.", readonly=True)

    # @api.depends('res_model', 'res_id')
    # def _compute_res_name(self):
    #     for activity in self:
    #         activity.res_name = activity.res_model and \
    #             self.env[activity.res_model].browse(activity.res_id).display_name
    
    def test(self):
        raise UserError(_('nguyen duc tu'))