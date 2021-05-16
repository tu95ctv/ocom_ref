# -*- coding: utf-8 -*-
{
    'name': "NDT data test",
    'summary':"NDT data test",
    'version': '0.1',
    'website': "http://www.vidoo.vn",
    'author': "Nguyen Duc Tu",
    "license": "AGPL-3",
    'depends': ['base', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/cronjob_data.xml',
        'data/outgoing_mail.xml',
        'views/ndt_data_test.xml',
        'views/test_model_views.xml',
        'menu/menu.xml',
    ],
    "external_dependencies": {"python": []},
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}