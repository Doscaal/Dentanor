# Copyright 2020 Doscaal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    date_order = fields.Datetime(readonly=False, track_visibility='onchange')

    @api.model
    def create(self, values):
        if values.get('partner_id', False):
            public = self.env.ref('base.public_partner')
            if values['partner_id'] == public.id:
                raise UserError(_("Veuillez créer un compte"))
        return super(SaleOrder, self).create(values)
