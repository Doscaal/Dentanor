# Copyright 2020 Doscaal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    warehouse_id = fields.Many2one(comodel_name='stock.warehouse',
                                   string='Entrepôt')
