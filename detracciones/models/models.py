# -*- coding: utf-8 -*-

from odoo import models, fields, api

class detracciones(models.Model):
    _name = 'sunat.detracciones'
    _description = "Codigos de Detracciones"

    name = fields.Text(string="Descripción")
    detrac = fields.Integer(string="Detraccion")
    detracmack = fields.Char(string="Porcentaje",compute="_obtener_detraccion")

    def _obtener_detraccion(self):
        for rec in self:
            detrac = str(rec.detrac)
            rec.detracmack = "{}%".format(detrac)