# Copyright 2020 Doscaal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class IntrastatProductDeclaration(models.Model):
    _inherit = 'intrastat.product.declaration'

    def _xls_declaration_line_fields(self):
        res = super(IntrastatProductDeclaration,
                    self)._xls_declaration_line_fields()
        res.append('product_origin_country')
        return res
