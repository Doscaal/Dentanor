# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class PaymentLinkWizard(models.TransientModel):
    _inherit = "payment.link.wizard"

    website_id = fields.Many2one(comodel_name='website', string='Site web',
                                 readonly=True)

    @api.model
    def default_get(self, fields):
        res = super(PaymentLinkWizard, self).default_get(fields)
        res_id = self._context.get('active_id')
        res_model = self._context.get('active_model')
        if 'current_website_id' in self.env[res_model]._fields:
            record = self.env[res_model].browse(res_id)
            res.update({
                'website_id': record.current_website_id.id,
            })
        return res
