# -*- coding: utf-8 -*-
# from odoo import http


# class PartnerStakeholder(http.Controller):
#     @http.route('/partner_stakeholder/partner_stakeholder/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/partner_stakeholder/partner_stakeholder/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('partner_stakeholder.listing', {
#             'root': '/partner_stakeholder/partner_stakeholder',
#             'objects': http.request.env['partner_stakeholder.partner_stakeholder'].search([]),
#         })

#     @http.route('/partner_stakeholder/partner_stakeholder/objects/<model("partner_stakeholder.partner_stakeholder"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('partner_stakeholder.object', {
#             'object': obj
#         })
