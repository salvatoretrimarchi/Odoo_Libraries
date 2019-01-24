# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import itertools
from operator import itemgetter
import operator
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)


class bulk_invoice(models.TransientModel):
    _name = 'bulk.invoice'

    invoice_id = fields.Many2one('account.invoice', string='Invoice')
    partner_id = fields.Many2one('res.partner', string='Partner', readonly=True)
    amount = fields.Float('Amount', readonly=True)
    paid_amount = fields.Float('Pay Amount')
    bulk_invoice_id = fields.Many2one('bulk.inv.payment')
    bulk_detraction_id = fields.Many2one('bulk.inv.detraction')

    bank_id = fields.Char(string='Banco', readonly=True)


class bulk_inv_payment(models.TransientModel):
    _name = 'bulk.inv.payment'

    @api.model
    def default_get(self, fields):
        res = {}
        inv_ids = self._context.get('active_ids')
        vals = []
        invoice_ids = self.env['account.invoice'].browse(inv_ids)
        inv_type = ''
        for invo in invoice_ids:
            inv_type = invo.type
            break
        for inv in invoice_ids:
            if inv_type != inv.type:
                raise ValidationError('You must select only invoices or refunds.')
            if inv.state != 'open':
                raise ValidationError('Please Select Open Invoices.')
            vals.append((0, 0, {
                'invoice_id': inv and inv.id or False,
                'partner_id': inv and inv.partner_id.id or False,
                'amount': inv.residual or 0.0,
                'paid_amount': inv.residual or 0.0,
            }))
            if inv.type in ('out_invoice', 'out_refund'):
                res.update({
                    'partner_type': 'customer',
                })
            else:
                res.update({
                    'partner_type': 'supplier',
                })
        if inv_type in ('out_invoice', 'in_refund'):
            res.update({
                'payment_type': 'inbound'
            })
        else:
            res.update({
                'payment_type': 'outbound'
            })

        res.update({
            'invoice_ids': vals,
        })
        return res

    name = fields.Char('Name', default='hello')
    payment_type = fields.Selection(
        [('outbound', 'Send Money'), ('inbound', 'Receive Money'), ('transfer', 'Transfer')], string="Payment Type",
        required="1")
    payment_date = fields.Date('Payment Date', required="1")
    communication = fields.Char('Memo')
    partner_type = fields.Selection([('customer', 'Customer'), ('supplier', 'Supplier')], string='Partner Type')
    journal_id = fields.Many2one('account.journal', string='Payment Method', required=True,
                                 domain=[('type', 'in', ('bank', 'cash'))])
    invoice_ids = fields.One2many('bulk.invoice', 'bulk_invoice_id', string='Invoice')

    @api.multi
    def process_payment_(self):
        new_payment_ids = []

        # Lista de proveedores con sus facturas
        for rec in self:

            # Factura
            for inv_line in rec.invoice_ids:

                # Metodo de Pago
                payment_method_id = rec.env['account.payment.method'].search([('name', '=', 'Manual')], limit=1)

                # Si no se encuentra el metodo de pago busca otro
                if not payment_method_id:
                    payment_method_id = rec.env['account.payment.method'].search([], limit=1)

                # Declara Fecha de Pago
                payment_date = False

                # Si hay una fecha se la asigna a la variable anterior
                if rec.payment_date:
                    payment_date = rec.payment_date.strftime("%Y-%m-%d")

                _logger.info("Factura Resumida")
                _logger.info(inv_line)

                _logger.info("Factura")
                _logger.info(inv_line.invoice_id)

                # Plantillas para los pagos
                pago_valores_1 = {
                    'payment_type': rec.payment_type,
                    'payment_date': payment_date,
                    'partner_type': rec.partner_type,
                    'payment_for': 'multi_payment',
                    'partner_id': inv_line.partner_id and inv_line.partner_id.id or False,
                    'journal_id': rec.journal_id and rec.journal_id.id or False,
                    'communication': rec.communication,
                    'payment_method_id': payment_method_id and payment_method_id.id or False,
                    'state': 'draft',
                    'currency_id': inv_line.invoice_id.currency_id and inv_line.invoice_id.currency_id.id or False,
                    'amount': 0.0,
                    'line_ids': False,
                    'invoice_ids': False
                }

                _logger.info("pago_valores_1")
                _logger.info(pago_valores_1)

                _logger.info("se crea el registro del pago 1")
                pago_1 = rec.env['account.payment'].create(pago_valores_1)
                _logger.info(pago_1)

                pago_valores_2 = {
                    'payment_type': rec.payment_type,
                    'payment_date': payment_date,
                    'partner_type': rec.partner_type,
                    'payment_for': 'multi_payment',
                    'partner_id': inv_line.partner_id and inv_line.partner_id.id or False,
                    'journal_id': rec.journal_id and rec.journal_id.id or False,
                    'communication': rec.communication,
                    'payment_method_id': payment_method_id and payment_method_id.id or False,
                    'state': 'draft',
                    'currency_id': inv_line.invoice_id.currency_id and inv_line.invoice_id.currency_id.id or False,
                    'amount': 0.0,
                    'line_ids': False,
                    'invoice_ids': False
                }

                _logger.info("pago_valores_2")
                _logger.info(pago_valores_2)

                _logger.info("se crea el registro del pago 2")
                pago_2 = rec.env['account.payment'].create(pago_valores_2)
                _logger.info(pago_2)

                _logger.info("Se crean variables")
                # Declaran variables
                detalle_pago_1 = []
                detalle_pago_2 = []
                total_pago1 = 0
                total_pago2 = 0
                facturas_1 = []
                facturas_2 = []

                # Se obtiene la Factura
                invoice = inv_line.invoice_id

                facturas_1.append(invoice.id)
                facturas_2.append(invoice.id)

                _logger.info("Factura 1 y 2")
                _logger.info(facturas_1)
                _logger.info(facturas_2)

                full_reco_1 = False
                full_reco_2 = False

                if invoice.residual == inv_line.paid_amount:
                    full_reco_2 = True

                cantidad_pago_1 = (inv_line.paid_amount / 2)
                cantidad_pago_2 = inv_line.paid_amount - cantidad_pago_1

                _logger.info("Valores 1 y 2 -> " + str(cantidad_pago_1) + " - " + str(cantidad_pago_2))

                detalle_pago_1.append((0, 0, {
                    'invoice_id': invoice.id,
                    'account_id': invoice.account_id and invoice.account_id.id or False,
                    'date': invoice.date_invoice,
                    'due_date': invoice.date_due,
                    'original_amount': invoice.amount_total,
                    'balance_amount': invoice.residual,
                    'allocation': cantidad_pago_1,
                    'full_reconclle': full_reco_1,
                    'account_payment_id': pago_1 and pago_1.id or False
                }))

                _logger.info("detalle_pago_1")
                _logger.info(detalle_pago_1)

                total_pago1 = cantidad_pago_1

                _logger.info("total_pago1")
                _logger.info(total_pago1)

                _logger.info("Se actualizara las lineas , total a pagar y id de facturas del pago 1")
                pago_1.write({
                    'line_ids': detalle_pago_1,
                    'amount': total_pago1,
                    'invoice_ids': [(6, 0, facturas_1)]
                })

                _logger.info("Se va ejecutar el proceso post() - 1")
                pago_1.post()

                detalle_pago_2.append((0, 0, {
                    'invoice_id': invoice.id,
                    'account_id': invoice.account_id and invoice.account_id.id or False,
                    'date': invoice.date_invoice,
                    'due_date': invoice.date_due,
                    'original_amount': invoice.amount_total,
                    'balance_amount': invoice.residual,
                    'allocation': cantidad_pago_2,
                    'full_reconclle': full_reco_2,
                    'account_payment_id': pago_2 and pago_2.id or False
                }))

                _logger.info("detalle_pago_2")
                _logger.info(detalle_pago_2)

                total_pago2 = cantidad_pago_2

                _logger.info("total_pago2")
                _logger.info(total_pago2)

                _logger.info("Se actualizara las lineas , total a pagar y id de facturas del pago 2")
                pago_2.write({
                    'line_ids': detalle_pago_2,
                    'amount': total_pago2,
                    'invoice_ids': [(6, 0, facturas_2)]
                })

                _logger.info("Se va ejecutar el proceso post() - 1")
                pago_2.post()

                _logger.info("Se anaden a la lista de new_payment_ids")
                new_payment_ids.append(pago_1)
                new_payment_ids.append(pago_2)

        return True

    @api.multi
    def process_payment2(self):
        vals = []
        for line in self.invoice_ids:
            if line.paid_amount > 0.0:
                vals.append({
                    'invoice_id': line.invoice_id or False,
                    'partner_id': line.partner_id and line.partner_id.id or False,
                    'amount': line.amount or 0.0,
                    'paid_amount': line.paid_amount or 0.0,
                    'currency_id': line.invoice_id.currency_id.id or False,
                })
        new_vals = sorted(vals, key=itemgetter('partner_id'))
        groups = itertools.groupby(new_vals, key=operator.itemgetter('partner_id'))
        result = [{'partner_id': k, 'values': [x for x in v]} for k, v in groups]
        new_payment_ids = []
        for res in result:
            payment_method_id = self.env['account.payment.method'].search([('name', '=', 'Manual')], limit=1)
            if not payment_method_id:
                payment_method_id = self.env['account.payment.method'].search([], limit=1)
            payment_date = False
            if self.payment_date:
                payment_date = self.payment_date.strftime("%Y-%m-%d")
            pay_val = {
                'payment_type': self.payment_type,
                'payment_date': payment_date,
                'partner_type': self.partner_type,
                'payment_for': 'multi_payment',
                'partner_id': res.get('partner_id'),
                'journal_id': self.journal_id and self.journal_id.id or False,
                'communication': self.communication,
                'payment_method_id': payment_method_id and payment_method_id.id or False,
                'state': 'draft',
                'currency_id': res.get('values')[0].get('currency_id'),
                'amount': 0.0,
            }
            payment_id = self.env['account.payment'].create(pay_val)
            line_list = []
            paid_amt = 0
            inv_ids = []
            for inv_line in res.get('values'):
                invoice = inv_line.get('invoice_id')
                inv_ids.append(invoice.id)
                full_reco = False
                if invoice.residual == inv_line.get('paid_amount'):
                    full_reco = True
                line_list.append((0, 0, {
                    'invoice_id': invoice.id,
                    'account_id': invoice.account_id and invoice.account_id.id or False,
                    'date': invoice.date_invoice,
                    'due_date': invoice.date_due,
                    'original_amount': invoice.amount_total,
                    'balance_amount': invoice.residual,
                    'allocation': inv_line.get('paid_amount'),
                    'full_reconclle': full_reco,
                    'account_payment_id': payment_id and payment_id.id or False
                }))
                paid_amt += inv_line.get('paid_amount')
            payment_id.write({
                'line_ids': line_list,
                'amount': paid_amt,
                'invoice_ids': [(6, 0, inv_ids)]
            })
            payment_id.post()
            new_payment_ids.append(payment_id)
        return True

    @api.multi
    def process_payment(self):
        for rec in self:

            # Factura
            _logger.info("Facturas")
            for inv_line in rec.invoice_ids:
                _logger.info(inv_line)
                _logger.info(inv_line.invoice_id.id)

                # Metodo de Pago
                payment_method_id = rec.env['account.payment.method'].search([('name', '=', 'Manual')], limit=1)
                # Si no se encuentra el metodo de pago busca otro
                if not payment_method_id:
                    payment_method_id = rec.env['account.payment.method'].search([], limit=1)

                # Declara Fecha de Pago
                payment_date = False
                # Si hay una fecha se la asigna a la variable anterior
                if rec.payment_date:
                    payment_date = rec.payment_date.strftime("%Y-%m-%d")

                invoice = inv_line.invoice_id
                detalle_pago = {
                    'invoice_id': invoice.id,
                    'account_id': invoice.account_id and invoice.account_id.id or False,
                    'date': invoice.date_invoice,
                    'due_date': invoice.date_due,
                    'original_amount': invoice.amount_total,
                    'balance_amount': invoice.residual,
                    'full_reconclle': False,
                    # 'account_payment_id': cabezera.id or False
                }

                pago_valores = {
                    'payment_type': rec.payment_type,
                    'payment_date': payment_date,
                    'partner_type': rec.partner_type,
                    'payment_for': 'multi_payment',
                    'partner_id': inv_line.partner_id and inv_line.partner_id.id or False,
                    'journal_id': rec.journal_id and rec.journal_id.id or False,
                    'communication': rec.communication,
                    'payment_method_id': payment_method_id and payment_method_id.id or False,
                    'state': 'draft',
                    'currency_id': inv_line.invoice_id.currency_id and inv_line.invoice_id.currency_id.id or False,
                    'amount': 0.0,
                    'line_ids': False,
                    'invoice_ids': [(6, 0, [inv_line.invoice_id.id, ])]
                }

                p1 = pago_valores
                p2 = pago_valores

                detalle_pago['allocation'] = inv_line.paid_amount / 2
                p1['line_ids'] = [(0, 0, detalle_pago), ]

                detalle_pago['allocation'] = inv_line.paid_amount - (inv_line.paid_amount / 2)
                p2['line_ids'] = [(0, 0, detalle_pago), ]

                inv_line.invoice_id.write({
                    'payment_ids': [(0, 0, [p1, p2])]
                })

                # pago = rec.env['account.payment']
                # pago1 = rec.env['account.payment'].create(p1)

                # pago1.write({
                #     #'line_ids': p1_lines,
                #     'line_ids': False,
                #     #'invoice_ids': [(6, 0, [inv_line.invoice_id.id, ])]
                #     'invoice_ids': False
                # })
                #
                # pago2 = rec.env['account.payment'].create(p2)
                # pago2.write({
                #     'line_ids': False,
                #     #'line_ids': p2_lines,
                #     #'invoice_ids': [(6, 0, [inv_line.invoice_id.id, ])]
                #     'invoice_ids': False
                # })
                _logger.info(p1)
                _logger.info(p2)


class bulk_inv_detraction(models.TransientModel):
    _name = 'bulk.inv.detraction'

    @api.model
    def default_get(self, fields):
        res = {}
        inv_ids = self._context.get('active_ids')
        vals = []
        invoice_ids = self.env['account.invoice'].browse(inv_ids)
        inv_type = ''
        for invo in invoice_ids:
            inv_type = invo.type
            break
        for inv in invoice_ids:
            if inv_type != inv.type:
                raise ValidationError('You must select only invoices or refunds.')
            if inv.state != 'open':
                raise ValidationError('Please Select Open Invoices.')
            if inv.detraccion_paid == True:
                raise ValidationError('Sólo facturas sin pago de detracción')

            # Obtener Cuenta Bancaria
            cuenta_bank_detrac = ""
            for rec in inv.partner_id.bank_ids:
                if rec.is_detraction:
                    cuenta_bank_detrac = rec.bank_id.name + " - " + rec.bank_id.bic

            vals.append((0, 0, {
                'invoice_id': inv and inv.id or False,
                'partner_id': inv and inv.partner_id.id or False,
                'amount': inv.residual or 0.0,
                'bank_id': cuenta_bank_detrac or '',
                'paid_amount': inv.detraction_residual or 0.0,
            }))
            if inv.type in ('out_invoice', 'out_refund'):
                res.update({
                    'partner_type': 'customer',
                })
            else:
                res.update({
                    'partner_type': 'supplier',
                })
        if inv_type in ('out_invoice', 'in_refund'):
            res.update({
                'payment_type': 'inbound'
            })
        else:
            res.update({
                'payment_type': 'outbound'
            })

        res.update({
            'invoice_ids': vals,
        })
        return res

    name = fields.Char('Name', default='hello')
    payment_type = fields.Selection(
        [('outbound', 'Send Money'), ('inbound', 'Receive Money'), ('transfer', 'Transfer')], string="Payment Type",
        required="1")
    payment_date = fields.Date('Payment Date', required="1")
    communication = fields.Char('Memo')
    partner_type = fields.Selection([('customer', 'Customer'), ('supplier', 'Supplier')], string='Partner Type')
    journal_id = fields.Many2one('account.journal', string='Payment Method', required=True,
                                 domain=[('type', 'in', ('bank', 'cash'))])
    invoice_ids = fields.One2many('bulk.invoice', 'bulk_detraction_id', string='Invoice')

    @api.multi
    def process_payment(self):
        vals = []
        for line in self.invoice_ids:
            if line.paid_amount > 0.0:
                vals.append({
                    'invoice_id': line.invoice_id or False,
                    'partner_id': line.partner_id and line.partner_id.id or False,
                    'amount': line.amount or 0.0,
                    'paid_amount': line.paid_amount or 0.0,
                    'currency_id': line.invoice_id.currency_id.id or False,
                })
        new_vals = sorted(vals, key=itemgetter('partner_id'))
        groups = itertools.groupby(new_vals, key=operator.itemgetter('partner_id'))
        result = [{'partner_id': k, 'values': [x for x in v]} for k, v in groups]
        new_payment_ids = []

        # Inicio de Modificado
        correlativo = 0
        pago_anterior = self.env['account.payment'].search([], order="id desc", limit=1)
        if pago_anterior.number_payment:
            correlativo = pago_anterior.number_payment + 1
        else:
            correlativo = 1
        # Fin de Modificado

        for res in result:
            payment_method_id = self.env['account.payment.method'].search([('name', '=', 'Manual')], limit=1)
            if not payment_method_id:
                payment_method_id = self.env['account.payment.method'].search([], limit=1)
            payment_date = False
            if self.payment_date:
                payment_date = self.payment_date.strftime("%Y-%m-%d")
            pay_val = {
                'payment_type': self.payment_type,
                'payment_date': payment_date,
                'partner_type': self.partner_type,
                'payment_for': 'multi_payment',
                'partner_id': res.get('partner_id'),
                'journal_id': self.journal_id and self.journal_id.id or False,
                'communication': self.communication,
                'payment_method_id': payment_method_id and payment_method_id.id or False,
                'state': 'draft',
                'number_payment': correlativo or 0,
                'currency_id': res.get('values')[0].get('currency_id'),
                'amount': 0.0,
            }
            payment_id = self.env['account.payment'].create(pay_val)
            line_list = []
            paid_amt = 0
            inv_ids = []
            for inv_line in res.get('values'):
                invoice = inv_line.get('invoice_id')
                inv_ids.append(invoice.id)
                full_reco = False
                if invoice.residual == inv_line.get('paid_amount'):
                    full_reco = True
                line_list.append((0, 0, {
                    'invoice_id': invoice.id,
                    'account_id': invoice.account_id and invoice.account_id.id or False,
                    'date': invoice.date_invoice,
                    'due_date': invoice.date_due,
                    'original_amount': invoice.amount_total,
                    'balance_amount': invoice.residual,
                    'allocation': inv_line.get('paid_amount'),
                    'full_reconclle': full_reco,
                    'account_payment_id': payment_id and payment_id.id or False
                }))
                paid_amt += inv_line.get('paid_amount')
            payment_id.write({
                'line_ids': line_list,
                'amount': paid_amt,
                'invoice_ids': [(6, 0, inv_ids)]
            })
            payment_id.post()
            new_payment_ids.append(payment_id)
        return True
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
