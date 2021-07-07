# -*- coding: utf-8 -*-
{
    "name": "msa_helpdesk",
    "summary": """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    "description": """
        Long description of module's purpose
    """,
    "author": "My Company",
    "website": "http://www.yourcompany.com",
    "category": "Uncategorized",
    "version": "14.0.1.0",
    # any module necessary for this one to work correctly
    "depends": ["base", "helpdesk"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/views.xml",
        "views/templates.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
}
