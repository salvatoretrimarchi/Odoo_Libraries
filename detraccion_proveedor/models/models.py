# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class proveedor(models.Model):
    _inherit = "res.partner"

    detrac_id = fields.Many2one('sunat.detracciones', 'Detraccion')


class account_invoice(models.Model):
    _inherit = "account.invoice"

    detrac_id = fields.Many2one('sunat.detracciones', 'Detraccion')
    detraccion = fields.Monetary(compute='_calcular_detrac',store=True)

    @api.onchange('partner_id')
    def _onchange_proveedor(self):
#        if len(self.detrac_id) <= 0 :
            self.detrac_id = self.partner_id.detrac_id

    
    @api.onchange('amount_total')
    def _calcular_detrac(self):
        self.detraccion = self.amount_total * (self.detrac_id.detrac / 100)


class detracciones(models.Model):
    _inherit = "sunat.detracciones"

    proveedor_ids = fields.One2many(
        'res.partner', 'detrac_id', 'Proveedores')
    factura_ids = fields.One2many(
        'account.invoice', 'detrac_id', 'Facturas')
