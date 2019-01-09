# -*- coding: utf-8 -*-

from odoo import models, fields, api


class proveedor(models.Model):
    _inherit = "res.partner"

    detrac_id = fields.Many2one('sunat.detracciones', 'Detraccion')


class account_invoice(models.Model):
    _inherit = "account.invoice"

    detrac_id = fields.Many2one('sunat.detracciones', 'Detraccion')
    detraccion = fields.Monetary(
        string="Detraccion", compute="_calcular_detrac", store=True)

    @api.onchange('partner_id')
    def _onchange_proveedor(self):
        #        if len(self.detrac_id) <= 0 :
        self.detrac_id = self.partner_id.detrac_id

    @api.depends('amount_total', 'detrac_id')
    @api.multi
    def _calcular_detrac(self):
        for record in self:
            record.detraccion = record.amount_total * \
                (record.detrac_id.detrac / 100)


class detracciones(models.Model):
    _inherit = "sunat.detracciones"

    proveedor_ids = fields.One2many(
        'res.partner', 'detrac_id', 'Proveedores')
    factura_ids = fields.One2many(
        'account.invoice', 'detrac_id', 'Facturas')
