# -*- coding: utf-8 -*-
{
    
    'name': "Odoo common template",
    'summary':"Odoo common template",
    'version': '0.1',
    'website': "http://www.vidoo.vn",
    'author': "Nguyen Duc Tu",
    "license": "AGPL-3",
    'depends': ['base','hr'],
    #'ndt_account_reports_inherit','ndt_close_entry': dùng để test tkdu và test kết chuyển
    'data': [
        'security/ir.model.access.csv',
        # 'data/cronjob_data.xml',
        'views/demo_view.xml',
    ],
    "external_dependencies": {"python": []},
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}