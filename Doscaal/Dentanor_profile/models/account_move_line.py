# Copyright 2020 Doscaal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    cost = fields.Float(string='Cout')
    margin = fields.Float(string='Marge(%)')
    margin_value = fields.Float(string='Marge')

    @api.onchange('product_id')
    def onchange_product_cost(self):
        if not self.product_id:
            self.cost = 0
        elif self.product_id in self.sale_line_ids.mapped('product_id'):
            self.cost = sum(self.sale_line_ids.mapped(
                'purchase_price')) / len(self.sale_line_ids) / self.quantity
        else:
            self.cost = self.product_id.standard_price

    @api.onchange('cost', 'price_unit')
    def onchange_price_unit(self):
        if self.price_unit:
            self.margin = (1 - self.cost / self.price_unit) * 100 or -100
            self.margin_value = (self.price_unit - self.cost) * self.quantity


class AccountMove(models.Model):
    _inherit = 'account.move'

    margin = fields.Float(string='Marge(%)', compute="compute_margin")
    margin_value = fields.Float(string='Marge', compute="compute_margin")

    def compute_margin(self):
        for inv in self:
            inv.margin_value = sum(inv.invoice_line_ids.mapped('margin_value'))
            if inv.amount_untaxed:
                inv.margin = inv.margin_value / (inv.amount_untaxed) * 100.
            else:
                inv.margin = 0

    @api.model
    def create(self, values):
        res = super(AccountMove, self).create(values)
        for line in res.invoice_line_ids:
            if line.sale_line_ids:
                if line.quantity:
                    line.cost = sum(line.sale_line_ids.mapped(
                        'purchase_price')) / len(
                            line.sale_line_ids) / line.quantity
                else:
                    line.cost = 0
            elif line.product_id:
                line.cost = line.product_id.standard_price
            else:
                line.cost = 0
            if line.price_unit:
                line.margin = (
                    1 - line.cost / line.price_unit) * 100 or -100
                line.margin_value = (
                    line.price_unit - line.cost) * line.quantity
        return res
