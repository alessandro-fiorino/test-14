# -*- coding: utf-8 -*-
# from odoo import http


# class MsaHelpdesk(http.Controller):
#     @http.route('/msa_helpdesk/msa_helpdesk/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/msa_helpdesk/msa_helpdesk/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('msa_helpdesk.listing', {
#             'root': '/msa_helpdesk/msa_helpdesk',
#             'objects': http.request.env['msa_helpdesk.msa_helpdesk'].search([]),
#         })

#     @http.route('/msa_helpdesk/msa_helpdesk/objects/<model("msa_helpdesk.msa_helpdesk"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('msa_helpdesk.object', {
#             'object': obj
#         })
