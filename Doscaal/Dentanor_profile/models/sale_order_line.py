# Copyright 2020 Doscaal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def _get_purchase_price(self, pricelist, product, product_uom, date):
        frm_cur = self.env.company.currency_id
        to_cur = pricelist.currency_id
        purchase_price = product.margin_cost
        if product_uom != product.uom_id:
            purchase_price = product.uom_id._compute_price(
                purchase_price, product_uom)
        price = frm_cur._convert(
            purchase_price, to_cur,
            self.order_id.company_id or self.env.company,
            date or fields.Date.today(), round=False)
        return {'purchase_price': price}

    def _compute_margin(self, order_id, product_id, product_uom_id):
        frm_cur = self.env.company.currency_id
        to_cur = order_id.pricelist_id.currency_id
        purchase_price = product_id.margin_cost
        if product_uom_id != product_id.uom_id:
            purchase_price = product_id.uom_id._compute_price(
                purchase_price, product_uom_id)
        price = frm_cur._convert(
            purchase_price, to_cur, order_id.company_id or self.env.company,
            order_id.date_order or fields.Date.today(), round=False)
        return price
