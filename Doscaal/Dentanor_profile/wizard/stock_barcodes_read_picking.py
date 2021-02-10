# Copyright 2019 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class WizStockBarcodesReadPicking(models.TransientModel):
    _inherit = "wiz.stock.barcodes.read.picking"

    move_line_ids = fields.Many2many(comodel_name='stock.move.line', store=False)

    @api.depends('picking_id.move_line_ids_without_package.qty_done')
    @api.onchange('picking_product_qty', 'barcode')
    def compute_move_lines(self):
        self.move_line_ids = self.picking_id.move_line_ids

    def process_barcode(self, barcode):
        res = super(WizStockBarcodesReadPicking, self).process_barcode(
            barcode)
        return res
