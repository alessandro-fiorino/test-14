# -*- coding: utf-8 -*-

from odoo import api, exceptions, fields, models


class PartnerStakeholder(models.Model):
    _name = "res.partner.stakeholder"
    _description = "Relazione tra partner ed entità generica"

    name = fields.Char(string="Descrizione", compute="_compute_name", compute_sudo=True)
    partner_id = fields.Many2one(
        string="Contatto",
        comodel_name="res.partner",
        ondelete="restrict",
        required=True,
    )
    res_model = fields.Char(string="Modello collegato", index=True, required=True)
    res_model_label = fields.Char(string="Modello", compute="_calc_label")
    res_id = fields.Many2oneReference(
        string="ID collegato", model_field="res_model", required=True
    )
    tag_ids = fields.Many2many(string="Etichette", comodel_name="res.partner.category")

    @api.depends("res_model", "res_id")
    def _compute_name(self):
        for r in self:
            r.name = r.res_model and self.env[r.res_model].browse(r.res_id).display_name

    @api.depends("res_model")
    def _calc_label(self):
        for r in self:
            r.res_model_label = (
                self.env["ir.model"].search([("model", "=", r.res_model)]).name
                if r.res_model
                else False
            )

    def action_open_related_record(self):
        self.ensure_one()
        if self.res_model and self.res_id:
            return self.env[self.res_model].browse(self.res_id).get_formview_action()
        return False


class PartnerStakeholderMixin(models.AbstractModel):
    _name = "res.partner.stakeholder.mixin"
    _description = "Mixin per collegare stakeholder ad un modello"

    ref_stakeholder_ids = fields.One2many(
        string="Stakeholder",
        comodel_name="res.partner.stakeholder",
        inverse_name="res_id",
        auto_join=True,
    )

    def unlink(self):
        """Override unlink to delete stakeholder records through (res_model, res_id)."""
        record_ids = self.ids
        result = super(PartnerStakeholderMixin, self).unlink()
        self.env["res.partner.stakeholder"].sudo().search(
            [("res_model", "=", self._name), ("res_id", "in", record_ids)]
        ).unlink()
        return result


class PartnerStakeHolderPartner(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner", "res.partner.stakeholder.mixin"]

    stakeholder_ids = fields.One2many(
        string="Stakeholder collegati",
        comodel_name="res.partner.stakeholder",
        inverse_name="partner_id",
        copy=False,
    )


class CrmLead(models.Model):
    _name = "crm.lead"
    _inherit = ["crm.lead", "res.partner.stakeholder.mixin"]


class ProjectProject(models.Model):
    _name = "project.project"
    _inherit = ["project.project", "res.partner.stakeholder.mixin"]


class ProjectTask(models.Model):
    _name = "project.task"
    _inherit = ["project.task", "res.partner.stakeholder.mixin"]
