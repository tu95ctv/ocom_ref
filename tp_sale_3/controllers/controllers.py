# -*- coding: utf-8 -*-
# from odoo import http


# class TpSale3(http.Controller):
#     @http.route('/tp_sale_3/tp_sale_3/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tp_sale_3/tp_sale_3/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tp_sale_3.listing', {
#             'root': '/tp_sale_3/tp_sale_3',
#             'objects': http.request.env['tp_sale_3.tp_sale_3'].search([]),
#         })

#     @http.route('/tp_sale_3/tp_sale_3/objects/<model("tp_sale_3.tp_sale_3"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tp_sale_3.object', {
#             'object': obj
#         })
