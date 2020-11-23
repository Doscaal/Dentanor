# Copyright 2020 Doscaal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    cost = fields.Float(string='Cout')
    margin = fields.Float(string='Marge(%)')

    @api.onchange('cost', 'price_unit')
    def onchange_price_unit(self):
        if self.price_unit:
            self.margin = (1 - self.cost / self.price_unit) * 100 or -100


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def create(self, values):
        res = super(AccountMove, self).create(values)
        for line in res.invoice_line_ids:
            if line.sale_line_ids:
                if line.quantity:
                    line.cost = sum(line.sale_line_ids.mapped(
                        'purchase_price')) / line.quantity
                else:
                    line.cost = 0
            elif line.product_id:
                line.cost = line.product_id.standard_price
            else:
                line.cost = 0
            if line.price_unit:
                line.margin = (
                    1 - line.cost / line.price_unit) * 100 or -100
        return res
