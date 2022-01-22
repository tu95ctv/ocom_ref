# -*- coding: utf-8 -*-
# from odoo import http


# class MySale(http.Controller):
#     @http.route('/my_sale/my_sale/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/my_sale/my_sale/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('my_sale.listing', {
#             'root': '/my_sale/my_sale',
#             'objects': http.request.env['my_sale.my_sale'].search([]),
#         })

#     @http.route('/my_sale/my_sale/objects/<model("my_sale.my_sale"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('my_sale.object', {
#             'object': obj
#         })
