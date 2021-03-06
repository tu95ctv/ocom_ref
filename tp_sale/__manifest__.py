# -*- coding: utf-8 -*-
{
    'name': "tp sale",
    'summary':"",
    'version': '0.1',
    'website': "http://www.vidoo.vn",
    'category': 'Human Resources/Tpsalesx10',
    'author': "Nguyen Duc Tu",
    "license": "AGPL-3",
    'depends': ['base','product','sale','website','website_form','report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/demo_data.xml',
        'data/email.xml',
        'data/ir_actions_server.xml',
        'data/data.xml',

        # 'views/demo_view.xml',
        'views/tp_sale.xml',
        'views/tp_sale2.xml',

        'views/tp_sale_line_views.xml',
        'views/menu.xml',
        'views/product_template.xml',
        'views/website_template.xml',
        'report/tp_sale_report.xml',
        'report/xlsx_report.xml'
    ],
    "external_dependencies": {"python": []},
}