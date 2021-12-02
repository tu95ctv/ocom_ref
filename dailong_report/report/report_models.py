# -*- coding: utf-8 -*-

# from odoo import models, fields, api
import ast
import copy
import json
import io
import logging
import lxml.html
import datetime
import ast
from collections import defaultdict
from math import copysign

from dateutil.relativedelta import relativedelta

from odoo.tools.misc import xlsxwriter
from odoo import models, fields, api, _
from odoo.tools import config, date_utils, get_lang
from odoo.osv import expression
from babel.dates import get_quarter_names
from odoo.tools.misc import formatLang, format_date
from odoo.addons.web.controllers.main import clean_action

_logger = logging.getLogger(__name__)
from odoo import models

class DaiLongReportXlsx(models.AbstractModel):
    _name = 'report.dailong_report.mo'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        for obj in objs:
            report_name = obj.name
            # One sheet by partner
            # sheet = workbook.add_worksheet(report_name[:31])
            # bold = workbook.add_format({'bold': True})
            # sheet.write(0, 0, obj.name, bold)
            options =  {'unfolded_lines': [], 'multi_company': [{'id': 1, 'name': 'CÔNG TY CỔ PHẦN NGUỒN NHÂN LỰC SIÊU VIỆT'}, {'id': 5, 'name': 'Company Tìm Việc Nhanh Fix Company hard code Onnet'}, {'id': 6, 'name': 'Công Ty Cổ Phần Dịch Vụ Tìm Việc Nhanh'}, {'id': 7, 'name': 'Công Ty Cổ Phần My Work'}, {'id': 8, 'name': 'Công Ty Cổ Phần Việc Làm 24h'}, {'id': 9, 'name': 'Công Ty Cổ Phần Việc Tốt Nhất'}, {'id': 13, 'name': 'company A'}, {'id': 14, 'name': 'company B'}], 'date': {'string': '2021', 'period_type': 'fiscalyear', 'mode': 'range', 'strict_range': False, 'date_from': '2021-01-01', 'date_to': '2021-12-31', 'filter': 'this_year'}, 'comparison': {'filter': 'no_comparison', 'number_period': 1, 'date_from': '', 'date_to': '', 'periods': []}, 'all_entries': False, 'analytic': True, 'analytic_accounts': [], 'selected_analytic_account_names': [], 'journals': [{'id': 'divider', 'name': 'Công Ty Cổ Phần Dịch Vụ Tìm Việc Nhanh'}, {'id': 11, 'name': 'Ghi nhận doanh thu', 'code': '3387R', 'type': 'general', 'selected': False}, {'id': 'divider', 'name': 'CÔNG TY CỔ PHẦN NGUỒN NHÂN LỰC SIÊU VIỆT'}, {'id': 7, 'name': 'Bank', 'code': 'BNK1', 'type': 'bank', 'selected': False}, {'id': 6, 'name': 'Cash', 'code': 'CSH1', 'type': 'cash', 'selected': False}, {'id': 5, 'name': 'Cash Basis Taxes', 'code': 'CABA', 'type': 'general', 'selected': False}, {'id': 1, 'name': 'Customer Invoices', 'code': 'INV', 'type': 'sale', 'selected': False}, {'id': 4, 'name': 'Exchange Difference', 'code': 'EXCH', 'type': 'general', 'selected': False}, {'id': 8, 'name': 'Inventory Valuation', 'code': 'STJ', 'type': 'general', 'selected': False}, {'id': 3, 'name': 'Miscellaneous Operations', 'code': 'MISC', 'type': 'general', 'selected': False}, {'id': 2, 'name': 'Vendor Bills', 'code': 'BILL', 'type': 'purchase', 'selected': False}], 'unfold_all': False, 'unposted_in_period': True, 'sorted_groupby_keys': [(0,)], 'headers': [[{'name': '', 'class': 'number', 'colspan': 1}, {'name': '2021', 'colspan': 1, 'key': 0, 'class': 'number'}, {'template': 'account_reports.cell_template_show_bug_financial_reports', 'style': 'width: 1%; text-align: right;'}]]}
            headers =[[{'name': 'Chỉ tiêu', 'style': 'width: 50%; text-align: right;'}, {'name': 'Mã', 'style': 'width: 20%; text-align: right;'}, {'name': '2021', 'colspan': 1, 'key': 0, 'class': 'number'}]]
            lines = [{'id': 2, 'name': 'Income', 'level': 0, 'class': 'o_account_reports_totals_below_sections', 'columns': [{'name': ''}, {'name': 11619000.0, 'no_format': 11619000.0, 'class': 'number'}], 'unfoldable': False, 'unfolded': True, 'page_break': False, 'action_id': False}, {'id': 3, 'name': 'Gross Profit', 'level': 2, 'class': 'o_account_reports_totals_below_sections', 'columns': [{'name': ''}, {'name': 11619000.0, 'no_format': 11619000.0, 'class': 'number'}], 'unfoldable': False, 'unfolded': True, 'page_break': False, 'action_id': False}, {'id': 4, 'name': 'Operating Income', 'level': 3, 'class': 'o_account_reports_totals_below_sections', 'columns': [{'name': ''}, {'name': 11619000.0, 'no_format': 11619000.0, 'class': 'number'}], 'unfoldable': True, 'unfolded': False, 'page_break': False, 'action_id': False}, {'id': 5, 'name': 'Cost of Revenue', 'level': 3, 'class': 'o_account_reports_totals_below_sections', 'columns': [{'name': ''}, {'name': 0.0, 'no_format': 0.0, 'class': 'number'}], 'unfoldable': False, 'unfolded': False, 'page_break': False, 'action_id': False}, {'id': 'total_3', 'name': 'Total Gross Profit', 'level': 3, 'parent_id': 3, 'class': 'total', 'columns': [{'name': ''}, {'name': 11619000.0, 'no_format': 11619000.0, 'class': 'number'}]}, {'id': 6, 'name': 'Other Income', 'level': 2, 'class': 'o_account_reports_totals_below_sections', 'columns': [{'name': ''}, {'name': -0.0, 'no_format': -0.0, 'class': 'number'}], 'unfoldable': False, 'unfolded': False, 'page_break': False, 'action_id': False}, {'id': 'total_2', 'name': 'Total Income', 'level': 1, 'parent_id': 2, 'class': 'total', 'columns': [{'name': ''}, {'name': 11619000.0, 'no_format': 11619000.0, 'class': 'number'}]}, {'id': 7, 'name': 'Expenses', 'level': 0, 'class': 'o_account_reports_totals_below_sections', 'columns': [{'name': ''}, {'name': 10489678.0, 'no_format': 10489678.0, 'class': 'number'}], 'unfoldable': False, 'unfolded': True, 'page_break': False, 'action_id': False}, {'id': 8, 'name': 'Expenses', 'level': 2, 'class': 'o_account_reports_totals_below_sections', 'columns': [{'name': ''}, {'name': 10489678.0, 'no_format': 10489678.0, 'class': 'number'}], 'unfoldable': True, 'unfolded': False, 'page_break': False, 'action_id': False}, {'id': 9, 'name': 'Depreciation', 'level': 2, 'class': 'o_account_reports_totals_below_sections', 'columns': [{'name': ''}, {'name': 0.0, 'no_format': 0.0, 'class': 'number'}], 'unfoldable': False, 'unfolded': False, 'page_break': False, 'action_id': False}, {'id': 'total_7', 'name': 'Total Expenses', 'level': 1, 'parent_id': 7, 'class': 'total', 'columns': [{'name': ''}, {'name': 10489678.0, 'no_format': 10489678.0, 'class': 'number'}]}, {'id': 1, 'name': 'Net Profit', 'level': 0, 'class': 'o_account_reports_totals_below_sections', 'columns': [{'name': ''}, {'name': 1129322.0, 'no_format': 1129322.0, 'class': 'number'}], 'unfoldable': False, 'unfolded': False, 'page_break': False, 'action_id': False}]
            self.get_xlsx(options, response=None,workbook=workbook, headers=headers, 
                lines = lines, obj = obj)
    
    def _get_cell_type_value(self, cell):
        if 'date' not in cell.get('class', '') or not cell.get('name'):
            # cell is not a date
            return ('text', cell.get('name', ''))
        if isinstance(cell['name'], (float, datetime.date, datetime.datetime)):
            # the date is xlsx compatible
            return ('date', cell['name'])
        try:
            # the date is parsable to a xlsx compatible date
            lg = self.env['res.lang']._lang_get(self.env.user.lang) or get_lang(self.env)
            return ('date', datetime.strptime(cell['name'], lg.date_format))
        except:
            # the date is not parsable thus is returned as text
            return ('text', cell['name'])


    def get_xlsx(self, options, response=None,workbook=None, headers=None, lines = None, obj=None):

        output = io.BytesIO()
        if not workbook:
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        # sheet = workbook.add_worksheet(self._get_report_name()[:31])
        sheet = workbook.add_worksheet('abc')
        date_default_col1_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'font_color': '#666666', 'indent': 2, 'num_format': 'yyyy-mm-dd'})
        date_default_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'font_color': '#666666', 'num_format': 'yyyy-mm-dd'})
        default_col1_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'font_color': '#666666', 'indent': 2})
        default_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'font_color': '#666666'})
        title_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'bottom': 2})
        level_0_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 13, 'bottom': 6, 'font_color': '#666666'})
        level_1_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 13, 'bottom': 1, 'font_color': '#666666'})
        level_2_col1_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 12, 'font_color': '#666666', 'indent': 1})
        level_2_col1_total_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 12, 'font_color': '#666666'})
        level_2_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 12, 'font_color': '#666666'})
        level_3_col1_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'font_color': '#666666', 'indent': 2})
        level_3_col1_total_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 12, 'font_color': '#666666', 'indent': 1})
        level_3_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'font_color': '#666666'})
        #Set the first column width to 50
        report_name_style = workbook.add_format({'font_name': 'Arial','font_size': 14, 'bold': True, 'font_color': 'red', 'align': 'center', 'valign': 'vcenter'})
        title_style_center_bold = workbook.add_format({'font_name': 'Arial', 'font_size': 10, 'bold': True, 'align': 'center', 'valign': 'vcenter'})
        sheet.set_column(0, 0, 50)
        y_offset = 0
        if not headers and lines :
            headers, lines = self.with_context(no_format=True, print_mode=True, prefetch_fields=False)._get_table(options)
        # print ('**options**', options)
        # print ('headers', headers)
        # print ('lines', lines)
        # Add headers.

        default_style1 = workbook.add_format({'font_name': 'Arial', 'font_size': 10, 'bold': 0})
        y_offset = 0
        x_offset = 0
        sheet.fit_to_pages(1, 0)
        sheet.set_column(1, 1, 5)
        sheet.set_column(2, 3, 10)

        sheet.write(y_offset, x_offset, self.env.company.display_name, default_style1)
        y_offset += 1
        sheet.write(y_offset, x_offset, self.env.company.street, default_style1)
        y_offset += 1
        sheet.write(y_offset, x_offset, obj.name, default_style1)
        y_offset += 1

        y_offset += 3
        merge_from = 'A'
        merge_to = 'E'
        report_title = ''
        report_title = 'LỆNH SẢN XUẤT'
        sheet.merge_range(merge_from + str(y_offset) + ':' + merge_to + str(y_offset), report_title, report_name_style)
        y_offset += 1


        for header in headers:
            x_offset = 0
            for column in header:
                column_name_formated = column.get('name', '').replace('<br/>', ' ').replace('&nbsp;', ' ')
                colspan = column.get('colspan', 1)
                if colspan == 1:
                    sheet.write(y_offset, x_offset, column_name_formated, title_style)
                else:
                    sheet.merge_range(y_offset, x_offset, y_offset, x_offset + colspan - 1, column_name_formated, title_style)
                x_offset += colspan
            y_offset += 1

        if options.get('hierarchy'):
            lines = self._create_hierarchy(lines, options)
        if options.get('selected_column'):
            lines = self._sort_lines(lines, options)
        # Add lines.
        for y in range(0, len(lines)):
            level = lines[y].get('level')
            if lines[y].get('caret_options'):
                style = level_3_style
                col1_style = level_3_col1_style
            elif level == 0:
                y_offset += 1
                style = level_0_style
                col1_style = style
            elif level == 1:
                style = level_1_style
                col1_style = style
            elif level == 2:
                style = level_2_style
                col1_style = 'total' in lines[y].get('class', '').split(' ') and level_2_col1_total_style or level_2_col1_style
            elif level == 3:
                style = level_3_style
                col1_style = 'total' in lines[y].get('class', '').split(' ') and level_3_col1_total_style or level_3_col1_style
            else:
                style = default_style
                col1_style = default_col1_style

            #write the first column, with a specific style to manage the indentation
            cell_type, cell_value = self._get_cell_type_value(lines[y])
            if cell_type == 'date':
                sheet.write_datetime(y + y_offset, 0, cell_value, date_default_col1_style)
            else:
                sheet.write(y + y_offset, 0, cell_value, col1_style)

            #write all the remaining cells
            for x in range(1, len(lines[y]['columns']) + 1):
                cell_type, cell_value = self._get_cell_type_value(lines[y]['columns'][x - 1])
                if cell_type == 'date':
                    sheet.write_datetime(y + y_offset, x + lines[y].get('colspan', 1) - 1, cell_value, date_default_style)
                else:
                    sheet.write(y + y_offset, x + lines[y].get('colspan', 1) - 1, cell_value, style)
        y_offset += y + 3
        sheet.write(y_offset, 3, 'Ngày ... tháng ... năm ...', default_style1)
        y_offset += 1
        sheet.write(y_offset, 0, "Người lập biểu                 Kế toán trưởng ", title_style_center_bold)
        sheet.write(y_offset, 3, "Giám đốc", title_style_center_bold)

        # workbook.close()
        # output.seek(0)
        # generated_file = output.read()
        # output.close()

        # return generated_file
        return workbook

    

