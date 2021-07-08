# -*- coding: utf-8 -*-
{
    "name": "massive_doc_import",
    "summary": """
        Importazione massiva documenti""",
    "description": """
        Importazone massiva documenti
    """,
    "author": "Alessandro Fiorino",
    "website": "http://www.digitaldomus.it",
    "category": "Uncategorized",
    "version": "14.0.1.0.0",
    # any module necessary for this one to work correctly
    "depends": ["base", "documents", "sale"],
    # always loaded
    "data": [
        "security/user_groups.xml",
        "security/ir.model.access.csv",
        "views/views.xml",
        "views/menues.xml",
        "data/documents.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
}
