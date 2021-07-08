# -*- coding: utf-8 -*-
{
    "name": "purchase_order_security",
    "summary": """
        Purchase order multi-level permission""",
    "description": """
        Purchase order multi-level permission
    """,
    #'author': "My Company",
    #'website': "http://www.yourcompany.com",
    "category": "Purchase",
    "version": "14.0.1.0",
    # any module necessary for this one to work correctly
    "depends": ["base", "purchase", "account", "stock"],
    # always loaded
    "data": [
        "security/purchase_security.xml",
        "security/ir.model.access.csv",
        "views/views.xml",
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    #'demo': [
    #    'demo/demo.xml',
    # ],
}
