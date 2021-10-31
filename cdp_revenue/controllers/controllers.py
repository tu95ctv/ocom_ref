# -*- coding: utf-8 -*-
# from odoo import http


# class CdpRevenue(http.Controller):
#     @http.route('/cdp_revenue/cdp_revenue/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cdp_revenue/cdp_revenue/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cdp_revenue.listing', {
#             'root': '/cdp_revenue/cdp_revenue',
#             'objects': http.request.env['cdp_revenue.cdp_revenue'].search([]),
#         })

#     @http.route('/cdp_revenue/cdp_revenue/objects/<model("cdp_revenue.cdp_revenue"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cdp_revenue.object', {
#             'object': obj
#         })
