# -*- coding: utf-8 -*-

from odoo import models, fields, api


class detracciones(models.Model):
    _name = 'sunat.detracciones'
    _description = "Codigos de Detracciones"
    _order = 'codigo'
    _rec_name = 'codigo'

    codigo = fields.Char(string="Código")
    desc = fields.Text(string="Descripción")
    detrac = fields.Float(string="Detraccion")