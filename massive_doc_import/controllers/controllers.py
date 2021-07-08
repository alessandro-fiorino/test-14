# -*- coding: utf-8 -*-
# from odoo import http


# class MassiveDocImport(http.Controller):
#     @http.route('/massive_doc_import/massive_doc_import/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/massive_doc_import/massive_doc_import/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('massive_doc_import.listing', {
#             'root': '/massive_doc_import/massive_doc_import',
#             'objects': http.request.env['massive_doc_import.massive_doc_import'].search([]),
#         })

#     @http.route('/massive_doc_import/massive_doc_import/objects/<model("massive_doc_import.massive_doc_import"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('massive_doc_import.object', {
#             'object': obj
#         })
