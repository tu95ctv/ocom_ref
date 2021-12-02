# -*- coding: utf-8 -*-
# from odoo import http


# class TestReport(http.Controller):
#     @http.route('/test_report/test_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test_report/test_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('test_report.listing', {
#             'root': '/test_report/test_report',
#             'objects': http.request.env['test_report.test_report'].search([]),
#         })

#     @http.route('/test_report/test_report/objects/<model("test_report.test_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test_report.object', {
#             'object': obj
#         })
