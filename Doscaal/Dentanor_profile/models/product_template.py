# Copyright 2020 Doscaal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_forfait = fields.Boolean(string='Est un forfait')
    margin_cost = fields.Float(
        'Coût de revient', compute='_compute_margin_cost',
        inverse='_set_margin_cost', store=True)
    margin = fields.Float('Marge', compute='_compute_margin_cost')
    margin_percent = fields.Float('Marge(%)', compute='_compute_margin_cost')

    @api.depends('product_variant_ids', 'product_variant_ids.margin_cost')
    def _compute_margin_cost(self):
        unique_variants = self.filtered(lambda template: len(
            template.product_variant_ids) == 1)
        for template in unique_variants:
            variant = template.product_variant_ids
            template.margin_cost = template.product_variant_ids.margin_cost
            template.margin = variant.list_price - variant.margin_cost
            template.margin_percent = (variant.list_price - variant.margin_cost
                                       ) / variant.list_price * 100
        for template in (self - unique_variants):
            template.margin_cost = 0
            template.margin = 0
            template.margin_percent = 0

    def _set_margin_cost(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.margin_cost = template.margin_cost

    def action_view_sale_order(self):
        action = self.env.ref(
            'sale.action_quotations_with_onboarding').read()[0]
        action['domain'] = [(
            'order_line.product_id', 'in', self.product_variant_ids.ids)]
        action['context'] = {
            'active_id': self._context.get('active_id'),
        }
        return action
