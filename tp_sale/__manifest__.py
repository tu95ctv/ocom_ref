# -*- coding: utf-8 -*-
{
    'name': "Bán hàng",
    'summary':"",
    'version': '0.1',
    'website': "http://www.vidoo.vn",
    'author': "Nguyen Duc Tu",
    "license": "AGPL-3",
    'depends': ['base','product','sale'],
    'data': [
        'security/ir.model.access.csv',
        # 'views/demo_view.xml',
        'views/tp_sale.xml',
        'views/tp_sale_line_views.xml',
        'views/sale.xml',
        'views/menu.xml',
        'report/tp_sale_report.xml',
        'report/xlsx_report.xml'
    ],
    "external_dependencies": {"python": []},
}