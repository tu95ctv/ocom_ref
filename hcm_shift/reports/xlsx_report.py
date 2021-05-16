import datetime
from odoo import models
try:
    import xlsxwriter
except ImportError:
    _logger.debug("Can not import xlsxwriter`.")
import json
import io

class PartnerXlsx(models.AbstractModel):
    _name = 'report.module_name.report_shift'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        # for obj in partners:
        #     report_name = obj.name
        #     # One sheet by partner
        #     sheet = workbook.add_worksheet(report_name[:31])
        #     bold = workbook.add_format({'bold': True})
        #     sheet.write(0, 0, obj.name, bold)
        self.get_xlsx(workbook, partners)


#     def _get_table(self):
#         header = [
#     [{
#         'name': ''
#     }, {
#         'name': 'Date',
#         'class': 'date'
#     }, {
#         'name': 'Communication'
#     }, {
#         'name': 'Partner'
#     }, {
#         'name': 'Debit',
#         'class': 'number'
#     }, {
#         'name': 'Credit',
#         'class': 'number'
#     }, {
#         'name': 'Balance',
#         'class': 'number'
#     }]
# ]       
#         lines = [{
#     'id': 'account_12',
#     'name': '131 Trade receivables',
#     'title_hover': '131 Trade receivables',
#     'columns': [{
#         'name': 33000.0,
#         'class': 'number'
#     }, {
#         'name': 0.0,
#         'class': 'number'
#     }, {
#         'name': 33000.0,
#         'class': 'number'
#     }],
#     'level': 2,
#     'unfoldable': True,
#     'unfolded': True,
#     'colspan': 4,
#     'class': ''
# }, {
#     'id': 'initial_12',
#     'class': 'o_account_reports_initial_balance',
#     'name': 'Initial Balance',
#     'parent_id': 'account_12',
#     'columns': [{
#         'name': 0.0,
#         'class': 'number'
#     }, {
#         'name': 0.0,
#         'class': 'number'
#     }, {
#         'name': 0.0,
#         'class': 'number'
#     }],
#     'colspan': 4
# }, {
#     'id': 2,
#     'caret_options': 'account.move',
#     'class': 'top-vertical-align',
#     'parent_id': 'account_12',
#     'name': 'INV/2021/05/0001',
#     'columns': [{
#         'name': '05/02/2021',
#         'class': 'date'
#     }, {
#         'name': 'INV/2021/05/0001',
#         'title': 'INV/2021/05/0001',
#         'class': 'whitespace_print o_account_report_line_ellipsis'
#     }, {
#         'name': 'Nguyễn Võ Tuấn Thành',
#         'title': 'Nguyễn Võ Tuấn Thành',
#         'class': 'whitespace_print'
#     }, {
#         'name': 33000.0,
#         'class': 'number'
#     }, {
#         'name': '',
#         'class': 'number'
#     }, {
#         'name': 33000.0,
#         'class': 'number'
#     }],
#     'level': 2
# }, {
#     'id': 'account_143',
#     'name': '5111 Revenue from sales of merchandises',
#     'title_hover': '5111 Revenue from sales of merchandises',
#     'columns': [{
#         'name': 0.0,
#         'class': 'number'
#     }, {
#         'name': 33000.0,
#         'class': 'number'
#     }, {
#         'name': -33000.0,
#         'class': 'number'
#     }],
#     'level': 2,
#     'unfoldable': True,
#     'unfolded': False,
#     'colspan': 4,
#     'class': ''
# }, {
#     'id': 'general_ledger_total_1',
#     'name': 'Total',
#     'class': 'total',
#     'level': 1,
#     'columns': [{
#         'name': 33000.0,
#         'class': 'number'
#     }, {
#         'name': 33000.0,
#         'class': 'number'
#     }, {
#         'name': 0.0,
#         'class': 'number'
#     }],
#     'colspan': 4
# }]  
#         return header, lines

#     def _get_table(self):
#         header = [
#     [{
#         'name': ''
#     }, 
#     {
#         'name': 'Thời gian bắt đầu',
#         'class': 'datetime'
#     },
#     {
#         'name': 'Thời gian bắt kết thúc',
#         'class': 'datetime'
#     },
    
#     {
#         'name': 'Nội dung',
#     },
    


#     ]
# ]       
#         lines = [{
#     'id': 'account_12',
#     'name': 'Sự cố',
#     'title_hover': '131 Trade receivables',
#     'columns': [],
#     'level': 2,
#     'unfoldable': True,
#     'unfolded': True,
#     'colspan': 4,
#     'class': ''
# }, {
#     'id': 'initial_12',
#     'class': 'o_account_reports_initial_balance',
#     'name': 'Trạm 137',
#     'parent_id': 'account_12',
#     'columns': [],
#     'colspan': 4
# }, {
#     'id': 2,
#     'caret_options': 'account.move',
#     'class': 'top-vertical-align',
#     'parent_id': 'account_12',
#     'name': '',
#     'columns': [{
#         'name': '05/02/2021',
#         'class': 'datetime'
#     },
#     {
#         'name': '05/02/2021',
#         'class': 'datetime'
#     },
        
#      {
#         'name': 'Đối tác ra vào trạm thoải mái quá',
#     },


    
    
#     ],
#     'level': 2
# }, {
#     'id': 'account_143',
#     'name': '5111 Revenue from sales of merchandises',
#     'title_hover': '5111 Revenue from sales of merchandises',
#     'columns': [{
#         'name': 0.0,
#         'class': 'number'
#     }, {
#         'name': 33000.0,
#         'class': 'number'
#     }, {
#         'name': -33000.0,
#         'class': 'number'
#     }],
#     'level': 2,
#     'unfoldable': True,
#     'unfolded': False,
#     'colspan': 4,
#     'class': ''
# }, {
#     'id': 'general_ledger_total_1',
#     'name': 'Total',
#     'class': 'total',
#     'level': 1,
#     'columns': [{
#         'name': 33000.0,
#         'class': 'number'
#     }, {
#         'name': 33000.0,
#         'class': 'number'
#     }, {
#         'name': 0.0,
#         'class': 'number'
#     }],
#     'colspan': 4
# }]  
#         return header, lines


        
    def _get_report_name(self):
        return 'abc'

    def _get_cell_type_value(self, cell):
        if 'date' not in cell.get('class', '') or not cell.get('name'):
            # cell is not a date
            return ('text', cell.get('name', ''))
        if isinstance(cell['name'], (float, datetime.date, datetime.datetime)):
            # the date is xlsx compatible
            return ('date', cell['name'])
        try:
            # the date is parsable to a xlsx compatible date
            lg = self.env['res.lang']._lang_get(self.env.user.lang) #or get_lang(self.env)
            return ('date', datetime.datetime.strptime(cell['name'], lg.date_format))
        except:
            # the date is not parsable thus is returned as text
            return ('text', cell['name'])

    def _get_columns_name(self):
        header = [ 
    [{
        'name': ''
    }, {
        'name': 'Date',
        'class': 'date'
    }, {
        'name': 'Communication'
    }, {
        'name': 'Partner'
    }, {
        'name': 'Debit',
        'class': 'number'
    }, {
        'name': 'Credit',
        'class': 'number'
    }, {
        'name': 'Balance',
        'class': 'number'
    }]
]   
        return header
#     def _ndt_header(self):
#         header = [
#     [{
#         'name': ''
#     }, {
#         'name': 'Date',
#         'class': 'date'
#     }, {
#         'name': 'Communication'
#     }, {
#         'name': 'Partner'
#     }, {
#         'name': 'Debit',
#         'class': 'number'
#     }, {
#         'name': 'Credit',
#         'class': 'number'
#     }, {
#         'name': 'Balance',
#         'class': 'number'
#     }]
# ]   
#         return header

    def _get_table(self, partners):
        lines =  partners.xlsx_gen_line()
        return self._get_columns_name(), lines

    def get_account_display(self, options):
        account_content = options.get('ndt_special_report_account_codes','')
        if isinstance(account_content, list):
            account_content = ', '.join(account_content)
    
        acc_disp = 'Tài khoản: %s; '%account_content if account_content else ''
        return acc_disp
    def get_range_date_display(self, options):
        date = options.get('date', {})
        date_from = date.get('date_from')
        date_to = date.get('date_to')
        if date_from and date_to:
            date_from  = datetime.datetime.strptime(date_from, '%Y-%m-%d').strftime('%d/%m/%Y')
            date_to  = datetime.datetime.strptime(date_to, '%Y-%m-%d').strftime('%d/%m/%Y')
            rs = 'Từ ngày %s đến ngày %s'%( date_from, date_to)
        else:
            rs = ''
        return rs

    def super_columns_style (self, workbook):
        super_col_def_style = workbook.add_format({'font_name': 'Arial'})
        report_name_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 20,
             'align': 'center', 'valign': 'vcenter'})
        account_style = workbook.add_format({'font_name': 'Arial', 'italic': True, 'font_size': 8, 'align': 'center', 'valign': 'vcenter'})

        super_col_styles = {'super_col_def_style': super_col_def_style,
                            'report_name_style':report_name_style,
                            'account_style':account_style
        }
        return super_col_styles

    
    # def _super_columns_list(self, workbook, options, ctx, report_name_new, len_header_columns):
    #     super_col_styles = self.super_columns_style(workbook)
    #     super_col_def_style = super_col_styles['super_col_def_style']
    #     report_name_style = super_col_styles['report_name_style']
    #     account_style = super_col_styles['account_style']
    #     merge_row0 = 3
    #     if merge_row0 >=len_header_columns:
    #         merge_row0 = len_header_columns - 1

    #     row01 = {'string': 'Ngày: %s'%datetime.datetime.today().strftime('%d/%m/%Y'),
    #             'x_offset': len_header_columns - merge_row0 , 'style': super_col_def_style,'merge': merge_row0
    #         }
    #     row02 = {'string': 'Người báo cáo: %s'%self.env.user.name,
    #             'x_offset': len_header_columns - merge_row0 , 'style': super_col_def_style,'merge': merge_row0
    #         }
        
    #     row03 = {'string': 'Công ty:%s'%self.env.user.company_id.name,
    #             'x_offset': len_header_columns - merge_row0 , 'style': super_col_def_style,'merge': merge_row0
    #         }

    #     row04 = {'string': 'Địa chỉ:%s'%(self.env.user.company_id.street or ""),
    #             'x_offset': len_header_columns - merge_row0 , 'style': super_col_def_style,'merge': merge_row0
    #         }
      
    #     row1 = {'string': report_name_new,
    #             'x_offset': 0,'merge': len_header_columns, 'y_merge_offset':1, 'style': report_name_style,
    #         }

    #     # ghi dòng định khoản nhỏ 
    #     acc_disp = self.get_account_display(options)
    #     date_display = self.get_range_date_display(options)
    #     row2 = \
    #                 {'string': '%s%s'%(acc_disp, date_display),
    #                 'x_offset': 0, 'merge': len_header_columns, 'style': account_style
    #                 }
        
    #     super_columns_list =  [row01, row02, row03,row04, row1, row2]
    #     return super_columns_list

    

    def _ndt_write_super_columns(self, workbook, super_columns_list, sheet, y_offset):

        super_col_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'align': 'center'})
        
        for super_columnss in super_columns_list:
            if not isinstance(super_columnss, tuple):
                super_columnss = (super_columnss,)
            y_offset_before = y_offset
            y_merge_offset_max_one_row = 0
            for i, super_columns in enumerate(super_columnss):
                y_offset = y_offset_before
                if i == 0:
                    super_y_off = super_columns.get('super_y_off', 0)
                x = super_columns.get('x_offset', 0)
                y_offset += super_y_off
                style = super_columns.get('style', super_col_style)
                cell_content = super_columns.get('string', '').replace('<br/>', ' ').replace('&nbsp;', ' ')
                style = super_columns.get('style', style)
                x_merge = super_columns.get('merge', 0)
                y_merge_offset = super_columns.get('y_merge_offset', 0)
                if y_merge_offset > y_merge_offset_max_one_row:
                    y_merge_offset_max_one_row = y_merge_offset
                if x_merge or y_merge_offset:
                    sheet.merge_range(y_offset, x, y_offset + y_merge_offset, x + x_merge , cell_content, style)
                    x += x_merge
                    # y_offset +=y_merge_offset
                else:
                    sheet.write(y_offset, x, cell_content, style)
                    x += 1
            y_offset += y_merge_offset_max_one_row + 1
        return y_offset

    def _super_columns_list(self, workbook, options, ctx, report_name_new, len_header_columns):
        # TRUNG TÂM HẠ TẦNG MẠNG MIỀN NAM

        super_col_styles = self.super_columns_style(workbook)
        super_col_def_style = super_col_styles['super_col_def_style']
        report_name_style = super_col_styles['report_name_style']
        account_style = super_col_styles['account_style']


        row01 = {'string': 'TRUNG TÂM HẠ TẦNG MẠNG MIỀN NAM',
                'x_offset':0,'super_y_off':0,  'style': super_col_def_style,
            }
        row02 = {'string': 'CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM',
                'x_offset':4 
            }

        row11 = {'string': 'ĐÀI VIỄN THÔNG HỒ CHÍ MINH',
                'x_offset':0,'super_y_off':0
            }
        row12 = {'string': 'Độc lập - Tự do - Hạnh phúc',
                'x_offset':4
            }

        super_columns_list =  [(row01, row02), (row11, row12)]
        return super_columns_list



    def _under_columns_list(self, workbook):
        super_col_styles = self.super_columns_style(workbook)
        super_col_def_style = super_col_styles['super_col_def_style']
        report_name_style = super_col_styles['report_name_style']
        account_style = super_col_styles['account_style']


        row01 = {'string': 'TRƯỞNG ĐÀI VT HCM',
                'x_offset':0,'super_y_off':3,  'style': super_col_def_style,
            }
        row02 = {'string': 'Người làm báo cáo',
                'x_offset':4 
            }

        row11 = {'string': 'Ngô Hùng Thái',
                'x_offset':0,'super_y_off':3
            }
        row12 = {'string': 'Nguyễn Đức Tứ',
                'x_offset':4
            }

        super_columns_list =  [(row01, row02),(row11, row12)]
        return super_columns_list


	

    def get_xlsx(self, workbook=None, partners=None):
        # output = io.BytesIO()
        # workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet(self._get_report_name()[:31])
        

        # date_default_col1_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'font_color': '#666666', 'indent': 2, 'num_format': 'yyyy-mm-dd'})
        # date_default_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'font_color': '#666666', 'num_format': 'yyyy-mm-dd'})
        # default_col1_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'font_color': '#666666', 'indent': 2})
        # default_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'font_color': '#666666'})
        # title_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'bottom': 2, })
        # level_0_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 13, 'bottom': 6, 'font_color': '#666666'})
        # level_1_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 13, 'bottom': 1, 'font_color': '#666666'})
        # level_2_col1_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 12, 'font_color': '#666666', 'indent': })
        # level_2_col1_total_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 12, 'font_color': '#666666'})
        # level_2_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 12, 'font_color': '#666666'})
        # level_3_col1_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'font_color': '#666666', 'indent': 2})
        # level_3_col1_total_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 12, 'font_color': '#666666', 'indent': 1})
        # level_3_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'font_color': '#666666'})


        #######

        date_default_col1_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'indent': 2, 'num_format': 'yyyy-mm-dd', 'bottom': 2, 'top': 2, 'left': 2, 'right':2})
        date_default_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'num_format': 'yyyy-mm-dd', 'bottom': 2, 'top': 2, 'left': 2, 'right':2})
        default_col1_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'indent': 2, 'bottom': 2, 'top': 2, 'left': 2, 'right':2})
        default_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'bottom': 2, 'top': 2, 'left': 2, 'right':2})
        title_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'bottom': 2, 'top': 2, 'left': 2, 'right':2})
        level_0_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 13, 'bottom': 6, 'bottom': 2, 'top': 2, 'left': 2, 'right':2})#'bottom': 2, 'top': 2, 'left': 2,
        level_1_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 13, 
            'bottom': 1, 'bottom': 2, 'top': 2, 'left': 2, 'right':2})
        level_1_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'indent': 2, 'bottom': 2, 'top': 2, 'left': 2, 'right':2})
        level_2_col1_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 12, 'indent': 4,
            'bottom': 2, 'top': 2, 'left': 2, 'right':2})
        level_2_col1_total_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 12, 'bottom': 2, 'top': 2, 'left': 2, 'right':2})
        level_2_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 12, 'bottom': 2, 'top': 2, 'left': 2, 'right':2})
        level_3_col1_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'indent': 2, 'bottom': 2, 'top': 2, 'left': 2, 'right':2})
        level_3_col1_total_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 12, 'indent': 1, 'bottom': 2, 'top': 2, 'left': 2, 'right':2})
        level_3_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'bottom': 2, 'top': 2, 'left': 2, 'right':2})




        #Set the first column width to 50
        sheet.set_column(0, 0, 50)

        y_offset = 0
        # headers, lines = self.with_context(no_format=True, print_mode=True, prefetch_fields=False)._get_table(options)
        headers, lines = self.with_context(no_format=True, print_mode=True, prefetch_fields=False)._get_table(partners)

        # mới thêm
        options = {}
        ctx = {}
        report_name_new = 'TEST'
        len_header_columns = len(headers[0]) -1 
        super_columns_list = self._super_columns_list( workbook, options, ctx, report_name_new, len_header_columns)
        y_offset = 0
        y_offset = self._ndt_write_super_columns(workbook, super_columns_list, sheet, y_offset)
        
        y_offset += 1


        # Add headers.
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

        # if options.get('hierarchy'):
        #     lines = self._create_hierarchy(lines, options)
        # if options.get('selected_column'):
        #     lines = self._sort_lines(lines, options)

        # Add lines.
        if lines:
            max_width = max([len(l['columns']) + l.get('colspan',0) for l in lines])
        y = 0
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
                style = level_1_style
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
            
            for x in range(1, max_width - len(lines[y]['columns']) + 1):
                sheet.write(y + y_offset, x, None, style)

            #write all the remaining cells
            for x in range(1, len(lines[y]['columns']) + 1):
                cell_type, cell_value = self._get_cell_type_value(lines[y]['columns'][x - 1])
                if cell_type == 'date':
                    sheet.write_datetime(y + y_offset, x + lines[y].get('colspan', 1) - 1, cell_value, date_default_style)
                else:
                    sheet.write(y + y_offset, x + lines[y].get('colspan', 1) - 1, cell_value, style)
        y_offset = y + y_offset + 1

        super_columns_list = self._under_columns_list(workbook)
        y_offset = self._ndt_write_super_columns(workbook, super_columns_list, sheet, y_offset)


        # workbook.close()
        # output.seek(0)
        # generated_file = output.read()
        # output.close()

        # return generated_file

