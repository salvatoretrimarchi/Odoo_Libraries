# -*- coding: utf-8 -*-

from odoo import models, fields, api


class detracciones(models.Model):
    _name = 'sunat.detracciones'
    _description = "Codigos de Detracciones"

    codigo = fields.Char(string="Código")
    desc = fields.Text(string="Descripción")
    detrac = fields.Float(string="Detraccion")