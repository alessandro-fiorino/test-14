# -*- coding: utf-8 -*-

from odoo import api, exceptions, fields, models, tools


class Followers(models.Model):
    _inherit = "mail.followers"

    def _get_recipient_data(
        self, records, message_type, subtype_id, pids=None, cids=None
    ):
        res = super(Followers, self)._get_recipient_data(
            records, message_type, subtype_id, pids, cids
        )
        if (records) and (records._name == "helpdesk.ticket"):
            res2 = []
            for r in res:
                l = list(r)
                l[5] = "email"
                res2.append(tuple(l))
            return res2
        return res


class MessageSubtype(models.Model):
    _inherit = "mail.message.subtype"

    @tools.ormcache("self.env.uid", "self.env.su", "model_name")
    def _default_subtypes(self, model_name):
        sids, iids, eids = super(MessageSubtype, self)._default_subtypes(model_name)
        if model_name == "helpdesk.ticket":
            if 2 in sids:
                sids.remove(2)
            if 2 in iids:
                iids.remove(2)
            if 2 in eids:
                eids.remove(2)
        return sids, iids, eids


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    member_ids = fields.Many2many(related="team_id.member_ids")


class HelpdeskTag(models.Model):
    _inherit = "helpdesk.tag"

    team_id = fields.Many2one(
        comodel_name="helpdesk.team", string="Gruppo helpdesk", ondelete="restrict"
    )


class HelpdeskTicketType(models.Model):
    _inherit = "helpdesk.ticket.type"

    team_id = fields.Many2one(
        comodel_name="helpdesk.team", string="Gruppo helpdesk", ondelete="restrict"
    )


class HelpdeskTeam(models.Model):
    _inherit = "helpdesk.team"

    check_tags = fields.Boolean(string="Controllo presenza etichette", default=False)


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    tag_ids_N1 = fields.Many2one(
        "helpdesk.tag", string="Etichette N1", compute="_calc_Ntags", store=True
    )
    tag_ids_N2 = fields.Many2one(
        "helpdesk.tag", string="Etichette N2", compute="_calc_Ntags", store=True
    )
    tag_ids_N3 = fields.Many2one(
        "helpdesk.tag", string="Etichette N3", compute="_calc_Ntags", store=True
    )
    tag_ids_N4 = fields.Many2one(
        "helpdesk.tag", string="Etichette N4", compute="_calc_Ntags", store=True
    )
    tag_ids_N5 = fields.Many2one(
        "helpdesk.tag", string="Etichette N5", compute="_calc_Ntags", store=True
    )

    @api.constrains("stage_id", "user_id", "tag_ids_N1", "tag_ids_N2", "ticket_type_id")
    def _check_resolved_ticket(self):
        for r in self:
            if (r.stage_id) and (r.stage_id.name == "Risolto"):
                if not r.user_id:
                    raise exceptions.ValidationError("Utente assegnato a non impostato")
                if not r.ticket_type_id:
                    raise exceptions.ValidationError("Tipo ticket non impostato")
                if (r.team_id.check_tags) and (
                    (not r.tag_ids_N1) or (not r.tag_ids_N2) or (not r.tag_ids_N3)
                ):
                    raise exceptions.ValidationError(
                        "Primi tre livelli di etichette non impostate"
                    )

    @api.depends("tag_ids", "tag_ids.name")
    def _calc_Ntags(self):
        for r in self:
            r.tag_ids_N1 = r.tag_ids.filtered(lambda r: "1" in r.name.split()[0])
            r.tag_ids_N2 = r.tag_ids.filtered(lambda r: "2" in r.name.split()[0])
            r.tag_ids_N3 = r.tag_ids.filtered(lambda r: "3" in r.name.split()[0])
            r.tag_ids_N4 = r.tag_ids.filtered(lambda r: "4" in r.name.split()[0])
            r.tag_ids_N5 = r.tag_ids.filtered(lambda r: "5" in r.name.split()[0])
