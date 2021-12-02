# -*- coding: utf-8 -*-
# from odoo import http


# class TestAeroo(http.Controller):
#     @http.route('/test_aeroo/test_aeroo/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test_aeroo/test_aeroo/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('test_aeroo.listing', {
#             'root': '/test_aeroo/test_aeroo',
#             'objects': http.request.env['test_aeroo.test_aeroo'].search([]),
#         })

#     @http.route('/test_aeroo/test_aeroo/objects/<model("test_aeroo.test_aeroo"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test_aeroo.object', {
#             'object': obj
#         })
