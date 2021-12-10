# -*- coding: utf-8 -*-
# from odoo import http


# class NoFooter(http.Controller):
#     @http.route('/no_footer/no_footer/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/no_footer/no_footer/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('no_footer.listing', {
#             'root': '/no_footer/no_footer',
#             'objects': http.request.env['no_footer.no_footer'].search([]),
#         })

#     @http.route('/no_footer/no_footer/objects/<model("no_footer.no_footer"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('no_footer.object', {
#             'object': obj
#         })
