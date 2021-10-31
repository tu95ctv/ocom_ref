from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleLine(models.Model):
    _name = 'tp.sale.order.line'
    _description = 'TP sale'

    product_id = fields.Many2one('product.product', auto_join=1)
    qty = fields.Integer()
    price_unit = fields.Float(digits=(6,2))
    price = fields.Float(compute='_compute_price', store=True)
    order_id = fields.Many2one('tp.sale.order', ondelete='restrict')
    name = fields.Char()
    sale_ids = fields.Many2many('tp.sale.order','so_sol_rel','sol_id','so_id')
    
    @api.depends('qty', 'price_unit')
    def _compute_price(self):
        for record in self:
            record.price = record.qty * record.price_unit

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