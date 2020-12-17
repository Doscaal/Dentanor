# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    cost = fields.Float(string='Cout')
    margin_value = fields.Float(string='Marge')
    margin = fields.Float(string='Marge(%)', readonly=True,
                          group_operator="avg")

    @api.model
    def _select(self):
        res = super(AccountInvoiceReport, self)._select()
        res += ''',
           -line.balance / nullif(line.price_subtotal, 0.0) * line.cost *
           line.quantity as cost,
           -line.balance / nullif(line.price_subtotal, 0.0) * line.margin_value
           as margin_value,
           -line.balance / nullif(line.price_subtotal, 0.0) * line.margin
           as margin
        '''
        return res
