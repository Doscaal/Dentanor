# Copyright 2020 Doscaal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    margin = fields.Float(string='Marge', compute="compute_marge")
    margin_percent = fields.Float(string='Marge (%)', compute="compute_marge")
    margin_cost = fields.Float(string='Coût de revient',
                               company_dependent=True)
    standard_price = fields.Float(string='Valorisation')

    def compute_marge(self):
        for pp in self:
            pp.margin = pp.list_price - pp.margin_cost
            pp.margin_percent = (pp.list_price - pp.margin_cost
                                 ) / pp.list_price * 100
