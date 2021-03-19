# Copyright 2020 Doscaal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    def _validate_stock(self):
        previous_product_uom_qty = {
            line.id: line.product_uom_qty
            for line in self.sale_order_id.order_line}
        self.sale_order_id.order_line._action_launch_stock_rule(
            previous_product_uom_qty=previous_product_uom_qty)
        self.sale_order_id.picking_ids.filtered(
            lambda p: p.state == 'confirmed').action_assign()
        for picking in self.sale_order_id.picking_ids:
            for move in picking.move_lines.filtered(
                    lambda ml: ml.state != 'done'):
                for move_line in move.move_line_ids:
                    move_line.qty_done = move_line.product_uom_qty

        # context key used to not create backorders
        picking = self.sale_order_id.picking_ids.filtered(
            lambda p: p.state not in ['done', 'cancel'])
        picking.with_context(cancel_backorder=True).action_done()
