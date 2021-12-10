# -*- coding: utf-8 -*-
{
    'name': "no_footer",

    'summary': """
        no_footer""",

    'description': """
        no_footer
    """,

    'author': "Tienphong",
    'website': "Tienphong",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','website'],

    # always loaded
    'data': [
        'templates/layout.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
