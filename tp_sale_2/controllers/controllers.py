# -*- coding: utf-8 -*-
# from odoo import http


# class TpSale2(http.Controller):
#     @http.route('/tp_sale_2/tp_sale_2/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tp_sale_2/tp_sale_2/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tp_sale_2.listing', {
#             'root': '/tp_sale_2/tp_sale_2',
#             'objects': http.request.env['tp_sale_2.tp_sale_2'].search([]),
#         })

#     @http.route('/tp_sale_2/tp_sale_2/objects/<model("tp_sale_2.tp_sale_2"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tp_sale_2.object', {
#             'object': obj
#         })
