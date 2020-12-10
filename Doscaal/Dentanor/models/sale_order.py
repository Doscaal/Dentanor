# Copyright 2020 Doscaal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_margin_percent = fields.Float(string='Margin %',
                                    compute='compute_x_margin_percent')

    @api.depends('margin', 'amount_untaxed')
    def compute_x_margin_percent(self):
        for rec in self:
            if rec.amount_untaxed == 0.0:
                rec['x_margin_percent'] = None
            else:
                rec['x_margin_percent'] = 100*(rec.margin/rec.amount_untaxed)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    x_margin_percent = fields.Float(string='Margin %',
                                    compute='compute_x_margin_percent')

    @api.depends('price_subtotal', 'purchase_price', 'product_uom_qty')
    def compute_x_margin_percent(self):
        for rec in self:
            if rec.price_subtotal == 0.0 or rec.product_uom_qty == 0.0:
                rec['x_margin_percent'] = None
            else:
                price = rec.price_subtotal/rec.product_uom_qty
                rec['x_margin_percent'] = 100*(1 - rec.purchase_price/price)
