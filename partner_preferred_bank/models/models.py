# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PartnerPreferredBank(models.Model):
     _inherit = 'res.partner'

    property_preferred_incoming_bank_account_id=fields.Many2one(string="Preferred BA for receiving payments", comodel_name='res.partner.bank', company_dependant=True, domain="[('partner_id','=',user.company_id.id)]", help="Preferred bank account to be used for receiving payments from customers")
    property_preferred_outgoing_bank_account_id=fields.Many2one(string="Preferred BA for making payments", comodel_name='res.partner.bank', company_dependant=True, domain="[('partner_id','=',user.company_id.id)]", help="Preferred bank account to be used for making payments to suppliers" )
    property_preferred_riba_bank_account_id=fields.Many2one(string="Preferred customer BA for RIBA payments", comodel_name='res.partner.bank', company_dependant=True, domain="[('partner_id','=',id),('company_id','=',user.company_id.id)]", help="Preferred bank account of the customer to be used for RIBA payments" )
