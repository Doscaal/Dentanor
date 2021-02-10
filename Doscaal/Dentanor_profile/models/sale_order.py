# Copyright 2020 Doscaal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    date_order = fields.Datetime(readonly=False, track_visibility='onchange')
