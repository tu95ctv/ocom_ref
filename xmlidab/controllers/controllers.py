# -*- coding: utf-8 -*-
# from odoo import http


# class Xmlidab(http.Controller):
#     @http.route('/xmlidab/xmlidab/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/xmlidab/xmlidab/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('xmlidab.listing', {
#             'root': '/xmlidab/xmlidab',
#             'objects': http.request.env['xmlidab.xmlidab'].search([]),
#         })

#     @http.route('/xmlidab/xmlidab/objects/<model("xmlidab.xmlidab"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('xmlidab.object', {
#             'object': obj
#         })
