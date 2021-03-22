# Copyright 2020 Doscaal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_forfait = fields.Boolean(string='Est un forfait')

    def action_view_sale_order(self):
        action = self.env.ref(
            'sale.action_quotations_with_onboarding').read()[0]
        action['domain'] = [(
            'order_line.product_id', 'in', self.product_variant_ids.ids)]
        action['context'] = {
            'active_id': self._context.get('active_id'),
        }
        return action
