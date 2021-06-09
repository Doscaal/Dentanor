# Copyright 2020 Doscaal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    date_order = fields.Datetime(readonly=False, track_visibility='onchange')

    def _find_mail_template(self, force_confirmation_template=False):
        template_id = super(SaleOrder, self)._find_mail_template(
            force_confirmation_template)
        if force_confirmation_template or (
                self.state == 'sale' and not self.env.context.get(
                    'proforma', False)):
            template_id = int(self.env['ir.config_parameter'].sudo().get_param(
                'sale.default_confirmation_template_%s' % self.company_id.id))
            template_id = self.env['mail.template'].search(
                [('id', '=', template_id)]).id
            if not template_id:
                template_id = self.env['ir.model.data'].xmlid_to_res_id(
                    'sale.mail_template_sale_confirmation',
                    raise_if_not_found=False)

        return template_id
