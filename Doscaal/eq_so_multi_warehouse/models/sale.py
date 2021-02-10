# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 EquickERP
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.addons.sale_stock.report.sale_report import SaleReport
from collections import defaultdict


class sale_order(models.Model):
    _inherit = 'sale.order'

    @api.onchange('sale_order_template_id')
    def onchange_sale_order_template_id(self):
        res = super(sale_order, self).onchange_sale_order_template_id()
        for line in self.order_line:
            line.sol_warehouse_id = self.warehouse_id.id
        return res


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    sol_warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse")

    @api.depends('product_id', 'customer_lead', 'product_uom_qty', 'product_uom', 'order_id.warehouse_id', 'sol_warehouse_id', 'order_id.commitment_date')
    def _compute_qty_at_date(self):
        """ Compute the quantity forecasted of product at delivery date. There are
        two cases:
         1. The quotation has a commitment_date, we take it as delivery date
         2. The quotation hasn't commitment_date, we compute the estimated delivery
            date based on lead time"""
        qty_processed_per_product = defaultdict(lambda: 0)
        grouped_lines = defaultdict(lambda: self.env['sale.order.line'])
        # We first loop over the SO lines to group them by warehouse and schedule
        # date in order to batch the read of the quantities computed field.
        for line in self:
            if not line.display_qty_widget:
                continue
            line.warehouse_id = line.sol_warehouse_id
            if line.order_id.commitment_date:
                date = line.order_id.commitment_date
            else:
                date = line._expected_date()
            grouped_lines[(line.sol_warehouse_id.id, date)] |= line

        treated = self.browse()
        for (warehouse, scheduled_date), lines in grouped_lines.items():
            product_qties = lines.mapped('product_id').with_context(to_date=scheduled_date, warehouse=warehouse).read([
                'qty_available',
                'free_qty',
                'virtual_available',
            ])
            qties_per_product = {
                product['id']: (product['qty_available'], product['free_qty'], product['virtual_available'])
                for product in product_qties
            }
            for line in lines:
                line.scheduled_date = scheduled_date
                qty_available_today, free_qty_today, virtual_available_at_date = qties_per_product[line.product_id.id]
                line.qty_available_today = qty_available_today - qty_processed_per_product[line.product_id.id]
                line.free_qty_today = free_qty_today - qty_processed_per_product[line.product_id.id]
                line.virtual_available_at_date = virtual_available_at_date - qty_processed_per_product[line.product_id.id]
                if line.product_uom and line.product_id.uom_id and line.product_uom != line.product_id.uom_id:
                    line.qty_available_today = line.product_id.uom_id._compute_quantity(line.qty_available_today, line.product_uom)
                    line.free_qty_today = line.product_id.uom_id._compute_quantity(line.free_qty_today, line.product_uom)
                    line.virtual_available_at_date = line.product_id.uom_id._compute_quantity(line.virtual_available_at_date, line.product_uom)
                qty_processed_per_product[line.product_id.id] += line.product_uom_qty
            treated |= lines
        remaining = (self - treated)
        remaining.virtual_available_at_date = False
        remaining.scheduled_date = False
        remaining.free_qty_today = False
        remaining.qty_available_today = False
        remaining.warehouse_id = False

    def _prepare_procurement_values(self, group_id=False):
        res = super(sale_order_line, self)._prepare_procurement_values(group_id)
        if res:
            res.update({'warehouse_id': self.sol_warehouse_id or self.order_id.warehouse_id})
        return res

    @api.onchange('product_id')
    def onchange_product_id_custom(self):
        self.sol_warehouse_id = self.order_id.warehouse_id

    @api.depends('product_id', 'route_id', 'order_id.warehouse_id', 'sol_warehouse_id', 'product_id.route_ids')
    def _compute_is_mto(self):
        """ Verify the route of the product based on the warehouse
            set 'is_available' at True if the product availibility in stock does
            not need to be verified, which is the case in MTO, Cross-Dock or Drop-Shipping
        """
        self.is_mto = False
        for line in self:
            if not line.display_qty_widget:
                continue
            product = line.product_id
            product_routes = line.route_id or (product.route_ids + product.categ_id.total_route_ids)
            # Check MTO
            warehouse_id = line.sol_warehouse_id
            if not warehouse_id:
                warehouse_id = line.order_id.warehouse_id
            mto_route = warehouse_id.mto_pull_id.route_id
            if not mto_route:
                try:
                    mto_route = self.env['stock.warehouse']._find_global_route('stock.route_warehouse0_mto', _('Make To Order'))
                except UserError:
                    # if route MTO not found in ir_model_data, we treat the product as in MTS
                    pass

            if mto_route and mto_route in product_routes:
                line.is_mto = True
            else:
                line.is_mto = False


class sale_report(models.Model):
    _inherit = "sale.report"

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        sol_obj = self.env['sale.order.line'].sudo()
        if 'sol_warehouse_id' in sol_obj._fields:
            fields['warehouse_id'] = ", l.sol_warehouse_id as warehouse_id"
            groupby += ', l.sol_warehouse_id'
        else:
            fields['warehouse_id'] = ", s.warehouse_id as warehouse_id"
            groupby += ', s.warehouse_id'
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)

    SaleReport._query = _query

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: