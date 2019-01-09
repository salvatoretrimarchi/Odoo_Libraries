# -*- coding: utf-8 -*-

from odoo import models, fields, api


class detracciones(models.Model):
    _name = 'sunat.detracciones'
    _description = "Codigos de Detracciones"

    name = fields.Text(string="Description", translate=True)
    detrac = fields.Integer(string="Detraction", translate=True)
    detracmack = fields.Char(
        string="percentage", compute="_obtener_detraccion", translate=True)

    def _obtener_detraccion(self):
        for rec in self:
            detrac = str(rec.detrac)
            rec.detracmack = "{}%".format(detrac)


class tipo_doc(models.Model):
    _name = 'sunat.document_type'
    _description = "Tipos de Documentos"

    name = fields.Text(string="Description", translate=True)
    number = fields.Integer(string="Number", translate=True)


class account_invoice(models.Model):
    _inherit = "account.invoice"

    document_type_id = fields.Many2one('sunat.document_type', 'Document Type')
