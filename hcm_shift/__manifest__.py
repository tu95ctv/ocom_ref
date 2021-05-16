# -*- coding: utf-8 -*-
{
    'name': "HCM trực ca",
    'summary':"HCM trực ca",
    'description':"HCM trực ca",
    'version': '0.1',
    'website': "http://www.vidoo.vn",
    'author': "Nguyen Duc Tu",
    "license": "AGPL-3",
    'depends': ['base','report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'data/email.xml',
        'views/hcm_shift.xml',
        'views/shift_hour.xml',
        'reports/xlsx_report.xml',
    ],
    "external_dependencies": {"python": []},
}