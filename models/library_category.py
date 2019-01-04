# -*- coding: utf-8 -*-

from odoo import models, fields, api

class LibraryCategory(models.Model):
    _name = 'library.category'
    _description = "Categorias de los Libros"

    name = fields.Char(string="Nombre")
    active = fields.Boolean("Esta Activo")
