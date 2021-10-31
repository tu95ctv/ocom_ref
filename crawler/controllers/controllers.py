# -*- coding: utf-8 -*-
# from odoo import http


# class Crawler(http.Controller):
#     @http.route('/crawler/crawler/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/crawler/crawler/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('crawler.listing', {
#             'root': '/crawler/crawler',
#             'objects': http.request.env['crawler.crawler'].search([]),
#         })

#     @http.route('/crawler/crawler/objects/<model("crawler.crawler"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crawler.object', {
#             'object': obj
#         })
