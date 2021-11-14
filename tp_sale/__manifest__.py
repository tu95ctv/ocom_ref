# -*- coding: utf-8 -*-
{
    'name': "tp sale",
    'summary':"",
    'version': '0.1',
    'website': "http://www.vidoo.vn",
    'author': "Nguyen Duc Tu",
    "license": "AGPL-3",
    'depends': ['base','product','sale','website','website_form','report_xlsx','queue_job'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',

        'data/email.xml',

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