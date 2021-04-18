# Copyright 2020 Doscaal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    supplier_id = fields.Many2one(comodel_name='res.partner',
                                  string='Fournisseur', store=True,
                                  compute="compute_supplier")
    warehouse_id = fields.Many2one(comodel_name='stock.warehouse',
                                   string='Entrepôt', store=True,
                                   compute="compute_warehouse")

    def get_warehouse(self, location_id, whouses):
        if location_id.usage != 'internal':
            return False
        for whouse in whouses:
            if whouse.lot_stock_id == location_id:
                return whouse
        return self.get_warehouse(location_id.location_id, whouses)

    @api.depends('product_id')
    def compute_supplier(self):
        for quant in self:
            quant.supplier_id = quant.product_id.seller_ids and \
                quant.product_id.seller_ids[0].name or False

    @api.depends('location_id')
    def compute_warehouse(self):
        whouses = self.env['stock.warehouse'].search([])
        for quant in self:
            quant.warehouse_id = self.get_warehouse(quant.location_id, whouses)
