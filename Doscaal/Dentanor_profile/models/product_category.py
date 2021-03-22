# Copyright 2020 Doscaal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProductCategory(models.Model):
    _inherit = 'product.category'

    is_move_product = fields.Boolean(string='categorie de déplacement')
