# Copyright 2020 Doscaal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ProjectWorksheetTemplateDentanor(models.Model):
    _name = 'dentanor.project_worksheet_template'
    _description = 'modele pour les feuilles d intervention dentanor'

    x_name = fields.Char(string='Nom', size=64)
    x_task_id = fields.Many2one(comodel_name='project.task', string='Tâche')
    x_comments = fields.Text(string='Description')
    supplier_id = fields.Many2one(comodel_name='res.partner',
                                  string='Fournisseur')
    product_id = fields.Many2one(comodel_name='product.product',
                                 string='Produit')
    lot_id = fields.Many2one(comodel_name='stock.production.lot',
                             string='Numéro de série')
    move_product_id = fields.Many2one(comodel_name='product.product',
                                      string='Déplacement')
    is_forfait = fields.Boolean(string='Est un forfait',
                                computed="_compute_is_forfait")
    distance = fields.Integer(string='Distance', default=1)
    photo = fields.Binary(string='Photo')
    signature = fields.Binary(string='Signature technicien')
    sale_order_line_id = fields.Many2one(comodel_name='sale.order.line',
                                         string='Ligne de vente')

    @api.onchange('move_product_id')
    def _compute_is_forfait(self):
        for sheet in self:
            if sheet.move_product_id:
                sheet.is_forfait = sheet.move_product_id.is_forfait
            else:
                sheet.is_forfait = False

    @api.onchange('move_product_id')
    def onchange_move_product_id(self):
        if not self.move_product_id:
            self.distance = 1
        elif self.move_product_id.is_forfait:
            self.distance = 1

    def write(self, values):
        res = super(ProjectWorksheetTemplateDentanor, self).write(values)
        if not self.sale_order_line_id and values.get(
                'move_product_id', False):
            so = res.x_task_id.sale_order_id
            so.order_line = [
                (0, 0, {
                    'product_id': res.move_product_id.id,
                    'product_uom_qty': res.distance,
                })]
            res.sale_order_line_id = so.order_line.filtered(
                lambda sol: sol.product_id == res.move_product_id)
        elif values.get('move_product_id', False):
            self.sale_order_line_id.write({
                    'product_id': self.move_product_id.id,
                    'product_uom_qty': self.distance,
                })
            self.sale_order_line_id.product_id_change()
        elif values.get('distance'):
            self.sale_order_line_id.product_uom_qty = self.distance
        return res

    @api.model
    def create(self, values):
        if not values.get('x_name', False):
            values['x_name'] = self.env['project.task'].browse(
                values['x_task_id']).name
        res = super(ProjectWorksheetTemplateDentanor, self).create(values)
        if res.move_product_id:
            if not res.x_task_id.sale_order_id:
                res._fsm_ensure_sale_order()
            so = res.x_task_id.sale_order_id
            so.order_line = [
                (0, 0, {
                    'product_id': res.move_product_id.id,
                    'product_uom_qty': res.distance,
                })]
            res.sale_order_line_id = so.order_line.filtered(
                lambda sol: sol.product_id == res.move_product_id)
        return res
