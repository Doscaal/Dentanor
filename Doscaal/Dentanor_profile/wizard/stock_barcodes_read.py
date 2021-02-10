# Copyright 2019 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, models


class WizStockBarcodesRead(models.AbstractModel):
    _inherit = "wiz.stock.barcodes.read"
    _description = "Wizard to read barcode"

    def process_barcode(self, barcode):
        self._set_messagge_info("success", _("Barcode read correctly"))

        domain_picking = [('name', '=', barcode)]
        picking = self.env["stock.picking"].search(domain_picking)
        if picking:
            self.picking_id = picking
            self.candidate_picking_ids = [(0, 0, {'picking_id': picking.id})]
            return

        result = self.env['barcode.expression'].get_value(barcode)
        if result and 'product' in result.keys():
            domain = self._barcode_domain(result['product'])
        else:
            domain = self._barcode_domain(barcode)
        product = self.env["product.product"].search(domain)
        if product:
            if len(product) > 1:
                self._set_messagge_info("more_match", _(
                    "More than one product found"))
                return
            self.action_product_scaned_post(product)
            if product.tracking == 'none':
                self.action_done()
                return
        if self.env.user.has_group("product.group_stock_packaging"):
            packaging = self.env["product.packaging"].search(domain)
            if packaging:
                if len(packaging) > 1:
                    self._set_messagge_info(
                        "more_match", _("More than one package found")
                    )
                    return
                self.action_packaging_scaned_post(packaging)
                self.action_done()
                return

        if self.env.user.has_group("stock.group_production_lot"):
            if result and 'lot' in result.keys():
                lot_domain = [("name", "=", result['lot'])]
            else:
                lot_domain = [("name", "=", barcode)]
            if self.product_id:
                lot_domain.append(("product_id", "=", self.product_id.id))
            lot = self.env["stock.production.lot"].search(lot_domain)
            if len(lot) == 1:
                self.product_id = lot.product_id
            if not lot and self.product_id and self.product_id.tracking in (
                    'serial', 'lot') and result and result.get('lot', False):
                lot = self.env['stock.production.lot'].create({
                    'name': result['lot'],
                    'product_id': self.product_id.id,
                    'company_id': self.env.user.company_id.id,
                })
            if lot:
                self.action_lot_scaned_post(lot)
                self.action_done()
                return
        location = self.env["stock.location"].search(domain)
        if location:
            self.location_id = location
            self._set_messagge_info("info", _("Waiting product"))
            return
        self._set_messagge_info("not_found", _("Barcode not found"))
