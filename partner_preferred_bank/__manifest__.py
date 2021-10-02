# -*- coding: utf-8 -*-
{
    'name': "partner_preferred_bank",

    'summary': """
        Set the preferred bank for payments on a partner""",

    'description': """
        Set the preferred bank for payments on a partner
    """,

    'author': "Alessandro Fiorino <alessandro.fiorino@digitaldomus.it>",
    'website': "http://www.digitaldomus.it",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
