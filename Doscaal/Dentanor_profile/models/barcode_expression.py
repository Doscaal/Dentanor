# Copyright 2020 Doscaal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
import re


class BarcodeExpression(models.Model):
    _name = 'barcode.expression'
    _description = 'specific expression for barcode scanner'

    name = fields.Char(string='Name', size=64)
    expression = fields.Char(string='Label', size=128)
    sequence = fields.Integer(string='Sequence')

    def get_value(self, varchar):
        expressions = self.search([])
        for exp in expressions.sorted(key=lambda r: r.sequence):
            result = re.match(r"%s" % exp.expression, varchar)
            if result is not None:
                return result.groupdict()
        return False
