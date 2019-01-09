# -*- coding: utf-8 -*-

from odoo import models, fields, api

class detracciones(models.Model):
    _name = 'sunat.detracciones'
    _description = "Codigos de Detracciones"
    _order = 'codigo'

    name = fields.Char(string="Porcentaje",compute="_obtener_detraccion")
    codigo = fields.Char(string="Código")
    desc = fields.Text(string="Descripción")
    detrac = fields.Float(string="Detraccion")

    def _obtener_detraccion(self):
        for rec in self:
            detrac = str(rec.detrac)
            rec.name = "{} %".format(detrac)