# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.web.controllers.main import CSVExport,serialize_exception,ExcelExport
from odoo.exceptions import AccessError, UserError, AccessDenied

class CSVExportInh(CSVExport):
    @http.route('/web/export/csv', type='http', auth="user")
    @serialize_exception
    def index(self, data, token):
        raise UserError('TU DEP TRAI')
        return self.base(data, token)

class ExcelExportI(ExcelExport):

    @http.route('/web/export/xlsx', type='http', auth="user")
    @serialize_exception
    def index(self, data, token):
        params = json.loads(data)
        # raise UserError('TU DEP TRAI')
        return self.base(data, token)

# class ExportLimitGroup(http.Controller):
#     @http.route('/export_limit_group/export_limit_group/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/export_limit_group/export_limit_group/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('export_limit_group.listing', {
#             'root': '/export_limit_group/export_limit_group',
#             'objects': http.request.env['export_limit_group.export_limit_group'].search([]),
#         })

#     @http.route('/export_limit_group/export_limit_group/objects/<model("export_limit_group.export_limit_group"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('export_limit_group.object', {
#             'object': obj
#         })
