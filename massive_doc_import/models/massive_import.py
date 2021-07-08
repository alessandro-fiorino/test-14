# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, tools
from datetime import date, timedelta, datetime
import logging
import os

_logger = logging.getLogger(__name__)


class MassiveImportBatch(models.Model):
    _name = "documents.massive.batch"
    _description = "Batch di importazione massiva documenti"
    _inherit = ["mail.thread", "documents.mixin"]

    @api.model
    def _get_default_name(self):
        return "Batch %s utente %s" % (
            fields.Date.context_today(self),
            self.env.user.name,
        )

    name = fields.Char(string="Batch", default=lambda self: self._get_default_name())
    line_ids = fields.One2many(
        string="Elementi",
        comodel_name="documents.massive.batch.line",
        inverse_name="batch_id",
    )
    import_model = fields.Selection(
        string="Modello", selection=[("sale.order", "Offerte")], required=True
    )
    import_folder = fields.Many2one(
        string="Cartella", comodel_name="documents.folder", ondelete="set null"
    )
    default_tags = fields.Many2many(
        string="Etichette default", comodel_name="documents.tag", ondelete="cascade"
    )
    set_main = fields.Boolean(string="Imposta ad allegato principale", default=False)
    log = fields.Text(string="Log")
    remove_id = fields.Boolean(string="Rimuovi ID iniziale", default=False)
    match_field = fields.Char(string="Campo per ricerca id")

    def _get_document_folder(self):
        folder = self.env.ref("massive_doc_import.documents_temp_import")
        return folder

    def action_process_attachments(self):
        for r in self:
            r.line_ids.unlink()
            m_id = self.env["ir.model"].search([("model", "=", r.import_model)]).id
            for a in self.env["ir.attachment"].search(
                [("res_model", "=", "documents.massive.batch"), ("res_id", "=", r.id)]
            ):
                l = self.env["documents.massive.batch.line"].create(
                    {
                        "batch_id": r.id,
                        "attachment_id": a.id,
                        "import_model": r.import_model,
                        "import_folder": r.import_folder.id,
                        "set_main": r.set_main,
                        "default_tags": [(6, 0, r.default_tags.ids)],
                    }
                )
                if r.import_model:
                    (n, ext) = os.path.splitext(a.name)
                    n = n.split()[0]
                    k = self.env[r.import_model].search(
                        ["|", ("name", "=", n), ("name", "=ilike", n + " %")]
                    )
                    if len(k) > 0:
                        l.update(
                            {
                                "import_id": k.id,
                                r.import_model.replace(".", "_") + "_id": k.id,
                                "partner_id": k.partner_id.commercial_partner_id.id,
                            }
                        )
                    elif r.match_field:
                        k = self.env[r.import_model].search([(r.match_field, "=", n)])
                        if len(k) > 0:
                            l.update(
                                {
                                    "import_id": k.id,
                                    r.import_model.replace(".", "_") + "_id": k.id,
                                    "partner_id": k.partner_id.commercial_partner_id.id,
                                }
                            )

    def action_move_lines(self):
        todel = []
        for r in self:
            log = r.log or ""
            for d in self.line_ids:
                if d.import_id:
                    todel.append(d.id)
                    _logger.info("Attachment %s" % (d.attachment_id.name))
                    d.attachment_id.with_context(no_document=True).write(
                        {
                            "res_model": d.import_model,
                            "res_id": d.import_id,
                        }
                    )
                    if r.remove_id:
                        (n, ext) = os.path.splitext(d.attachment_id.name)
                        n = n.split(" ", 1)[1]
                        d.attachment_id.name = n + ext
                    doc = self.env["documents.document"].search(
                        [("attachment_id", "=", d.attachment_id.id)]
                    )
                    _logger.info("Doc %s" % (doc.name))
                    doc.write(
                        {
                            "res_model": d.import_model,
                            "res_id": d.import_id,
                            "folder_id": d.import_folder.id,
                            "tag_ids": [(6, 0, d.default_tags.ids)],
                        }
                    )
                    if d.set_main:
                        d.attachment_id.register_as_main_attachment()
                    log += "%s collegato a %s\n" % (
                        d.attachment_id.name,
                        self.env[d.import_model].browse(d.import_id).name,
                    )
            r.log = log
        if len(todel) > 0:
            self.env["documents.massive.batch.line"].browse(todel).unlink()


class MassiveImportBatchLine(models.Model):
    _name = "documents.massive.batch.line"
    _description = "Elenmento di batch importazione"

    batch_id = fields.Many2one(
        string="Batch", comodel_name="documents.massive.batch", ondelete="cascade"
    )
    attachment_id = fields.Many2one(
        string="Documento", comodel_name="ir.attachment", ondelete="cascade"
    )
    attachment_name = fields.Char(
        string="Nome Documento", related="attachment_id.name", readonly=False
    )
    attachment_type = fields.Selection(
        string="Tipo documento", related="attachment_id.type", readonly=False
    )
    import_model = fields.Selection(
        string="Modello", selection=[("sale.order", "Offerte")], required=True
    )
    import_folder = fields.Many2one(
        string="Cartella", comodel_name="documents.folder", ondelete="set null"
    )
    default_tags = fields.Many2many(
        string="Etichette default", comodel_name="documents.tag", ondelete="cascade"
    )
    import_id = fields.Integer(string="ID record")
    sale_order_id = fields.Many2one(
        string="Offerta", comodel_name="sale.order", ondelete="set null"
    )
    set_main = fields.Boolean(string="Imposta ad allegato principale", default=False)
    partner_id = fields.Many2one(
        string="Contatto", comodel_name="res.partner", ondelete="set null"
    )
    remove_id = fields.Boolean(related="batch_id.remove_id")

    @api.onchange("sale_order_id")
    def onchange_sale_order(self):
        for r in self:
            r.import_id = r.sale_order_id.id if r.sale_order_id else False

    def action_open_related_record(self):
        self.ensure_one()
        if self.import_model and self.import_id:
            return (
                self.env[self.import_model].browse(self.import_id).get_formview_action()
            )
        return False
