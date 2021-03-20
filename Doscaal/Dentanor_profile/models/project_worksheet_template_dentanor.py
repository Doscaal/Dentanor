# Copyright 2020 Doscaal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProjectWorksheetTemplateDentanor(models.Model):
    _name = 'dentanor.project_worksheet_template'

    x_name = fields.Char(string='Nom', size=64)
    x_task_id = fields.Many2one(comodel_name='project.task', string='Tâche')
    x_comments = fields.Text(string='Description')
    date = fields.Date(string='Date d\'intervention')
    supplier_id = fields.Many2one(comodel_name='res.partner',
                                  string='Fournisseur')
    product_id = fields.Many2one(comodel_name='product.product',
                                 string='Produit')
    lot_id = fields.Many2one(comodel_name='stock.production.lot',
                             string='Numéro de série')
    move_product_id = fields.Many2one(comodel_name='product.product',
                                      string='Déplacement')
    distance = fields.Integer(string='Distance')
    photo = fields.Binary(string='Photo')
    signature = fields.Binary(string='Signature technicien')
