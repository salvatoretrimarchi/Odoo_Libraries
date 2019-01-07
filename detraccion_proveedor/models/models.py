# -*- coding: utf-8 -*-

from odoo import models, fields, api


class proveedor(models.Model):
    _inherit = "res.partner"

    detrac_id = fields.Many2one('sunat.detracciones','Detraccion')


class account_invoice(models.Model):
    _inherit = "account.invoice"

    detrac_id = fields.Many2one('sunat.detracciones','Detraccion')


class detracciones(models.Model):
    _inherit = "sunat.detracciones"

    proveedor_ids = fields.One2many('res.partner', 'detrac_id', string="Proveedores")
    factura_ids = fields.One2many('account.invoice','detrac_id',string="Facturas")
