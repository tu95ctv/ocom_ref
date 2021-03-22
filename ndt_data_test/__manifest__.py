# -*- coding: utf-8 -*-
{
    
    'name': "NDT data test",
    'summary':"NDT data test",
    'version': '0.1',
    'website': "http://www.vidoo.vn",
    'author': "Nguyen Duc Tu",
    "license": "AGPL-3",
    'depends': ['base'],
    #'ndt_account_reports_inherit','ndt_close_entry': dùng để test tkdu và test kết chuyển
    'data': [
        'security/ir.model.access.csv',
        'data/cronjob_data.xml',

        'views/ndt_data_test.xml',
        'views/test_model_views.xml',
        
        'menu/menu.xml',
        # 'views/employee_views.xml',
        # 'views/ocom_template_view.xml'
    ],
    "external_dependencies": {"python": []},
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}