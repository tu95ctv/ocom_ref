# -*- coding: utf-8 -*-
# from odoo import http


# class Ece(http.Controller):
#     @http.route('/ece/ece/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ece/ece/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ece.listing', {
#             'root': '/ece/ece',
#             'objects': http.request.env['ece.ece'].search([]),
#         })

#     @http.route('/ece/ece/objects/<model("ece.ece"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ece.object', {
#             'object': obj
#         })
