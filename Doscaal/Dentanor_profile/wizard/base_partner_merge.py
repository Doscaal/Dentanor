# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class MergePartnerAutomatic(models.TransientModel):

    _inherit = 'base.partner.merge.automatic.wizard'

    def _merge(self, partner_ids, dst_partner=None, extra_checks=True):
        group = self.env.ref('Dentanor_profile.fusion_contact')
        if self.env.user in group.users:
            return super(MergePartnerAutomatic, self)._merge(
                partner_ids, dst_partner, False)
        else:
            return super(MergePartnerAutomatic, self)._merge(
                partner_ids, dst_partner, extra_checks)
