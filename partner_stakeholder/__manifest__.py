# -*- coding: utf-8 -*-
{
    "name": "partner_stakeholder",
    "summary": """
        Collegamento di elenchi di partner ad entità generiche""",
    "description": """
        Gestone partner stakeholder
    """,
    "author": "Alessandro Fiorino",
    "category": "Uncategorized",
    "version": "14.0.1.0.0",
    # any module necessary for this one to work correctly
    "depends": ["base", "crm", "project"],
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
