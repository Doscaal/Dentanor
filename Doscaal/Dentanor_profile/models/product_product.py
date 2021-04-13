# Copyright 2020 Doscaal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    margin_cost = fields.Float(string='Coût de revient')
