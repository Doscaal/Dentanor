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
        picking_ids = self.sale_order_id.picking_ids.filtered(
            lambda p: p.state == 'confirmed')
        if picking_ids:
            picking_ids.action_assign()
        for picking in self.sale_order_id.picking_ids:
            for move in picking.move_lines.filtered(
                    lambda ml: ml.state != 'done'):
                for move_line in move.move_line_ids:
                    move_line.qty_done = move_line.product_uom_qty

        # context key used to not create backorders
        picking = self.sale_order_id.picking_ids.filtered(
            lambda p: p.state not in ['done', 'cancel'])
        picking.with_context(cancel_backorder=True).action_done()

    def action_fsm_view_material(self):
        action = super(ProjectTask, self).action_fsm_view_material()
        if self.user_id.warehouse_id:
            action['context'].update({
                'search_default_warehouse_id': self.user_id.warehouse_id.id,
                'search_default_stock_available': 1})
        return action

    def action_fsm_view_order(self):
        action = self.env.ref('sale.action_quotations').read()[0]
        action.update({
            'name': self.name,
            'context': {
                'fsm_mode': True,
                'default_task_id': self.id,
                'default_partner_id': self.partner_id.id},
        })
        action['res_id'] = self.sale_order_id.id
        action['views'] = [(self.env.ref('sale.view_order_form').id, 'form')]
        return action

    def _fsm_create_sale_order(self):
        sale_order = super(ProjectTask, self)._fsm_create_sale_order()
        if self.user_id and self.user_id.warehouse_id:
            self.sale_order_id.write({
                'warehouse_id': self.user_id.warehouse_id.id,
            })
        return sale_order
