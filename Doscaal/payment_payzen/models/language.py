# coding: utf-8
#
# Copyright © Lyra Network.
# This file is part of PayZen plugin for Odoo. See COPYING.md for license details.
#
# Author:    Lyra Network (https://www.lyra.com)
# Copyright: Copyright © Lyra Network
# License:   http://www.gnu.org/licenses/agpl.html GNU Affero General Public License (AGPL v3)

from odoo import models, fields
from ..helpers import constants, tools

class PayzenLanguage(models.Model):
    _name = 'payzen.language'
    _description = 'PayZen language'
    _rec_name = 'label'
    _order = 'label'

    code = fields.Char()
    label = fields.Char(translate=tools.lang_translate)

    def init(self):
        languages = constants.PAYZEN_LANGUAGES

        for c, l in languages.items():
            lang = self.search([('code', '=', c)])

            if not lang:
                self.create({'code': c, 'label': l})
