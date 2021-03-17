# Copyright 2020 Doscaal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, _, fields
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    user_id = fields.Many2one(domain=[])

    def open_action_followup(self):
        compta = self.env.ref('account.group_account_manager')
        if compta not in self.env.user.groups_id:
            raise UserError(_(
                """Vous n'êtes pas autorisé à consulter les relances.
                Pour consulter les factures en cours, cliquez sur le bouton
                'Facturé' à droite de ce bouton"""))
        return super(ResPartner, self).open_action_followup()
