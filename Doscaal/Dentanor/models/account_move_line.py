# Copyright 2020 Doscaal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    cost = fields.Float(string='Cout')
    margin = fields.Float(string='Marge(%)')
    margin_value = fields.Float(string='Marge')

    @api.onchange('product_id')
    def onchange_product_cost(self):
        if not self.product_id:
            self.cost = 0
        elif self.product_id in self.sale_line_ids.mapped('product_id'):
            self.cost = sum(self.sale_line_ids.mapped(
                'purchase_price')) / len(self.sale_line_ids)
        else:
            self.cost = self.product_id.standard_price

    @api.onchange('cost', 'price_subtotal')
    def onchange_price_unit(self):
        if self.price_subtotal:
            self.margin = (1 - self.cost / (
                self.price_subtotal / self.quantity)) * 100
            self.margin_value = self.price_subtotal - (
                self.cost * self.quantity)
        elif not self.cost:
            self.margin = 0
            self.margin_value = 0
        else:
            self.margin = -100
            self.margin_value = -self.cost * self.quantity


class AccountMove(models.Model):
    _inherit = 'account.move'

    margin = fields.Float(string='Marge(%)', compute="compute_margin")
    margin_value = fields.Float(string='Marge', compute="compute_margin")

    def write(self, values):
        if values.get('invoice_line_ids', False):
            for data in values['invoice_line_ids']:
                if data[0] in (0, 1):
                    if data[2].get('cost', False):
                        my_dict = {'cost': data[2]['cost']}
                    else:
                        my_dict = {}
                    if data[2].get('margin', False):
                        my_dict.update({
                            'margin': data[2]['margin'],
                            'margin_value': data[2]['margin_value']
                        })
                    if values.get('line_ids', False):
                        for x in values['line_ids']:
                            if x[0] in (0, 1) and x[1] == data[1]:
                                x[2].update(my_dict)
                                break
                        else:
                            if data[0] == 1:
                                values['line_ids'].append([
                                    (data[0], data[1], my_dict)])
                    else:
                        if data[0] == 1:
                            values['line_ids'] = [(data[0], data[1], my_dict)]

        return super(AccountMove, self).write(values)

    @api.depends('invoice_line_ids.cost', 'invoice_line_ids.price_subtotal')
    def compute_margin(self):
        for inv in self:
            inv.margin_value = sum(inv.invoice_line_ids.mapped('margin_value'))
            if inv.amount_untaxed:
                inv.margin = inv.margin_value / (inv.amount_untaxed) * 100.
            else:
                inv.margin = 0

    @api.model
    def create(self, values):
        res = super(AccountMove, self).create(values)
        for line in res.invoice_line_ids:
            if line.sale_line_ids:
                if line.quantity:
                    line.cost = sum(line.sale_line_ids.mapped(
                        'purchase_price')) / len(
                            line.sale_line_ids)
                else:
                    line.cost = 0
            elif line.product_id:
                line.cost = line.product_id.standard_price
            else:
                line.cost = 0
            if line.price_subtotal:
                line.margin = (
                    1 - line.cost / (
                        line.price_subtotal / line.quantity)) * 100
                line.margin_value = line.price_subtotal - (
                    line.cost * line.quantity)
            elif not line.cost:
                line.margin = 0
                line.margin_value = 0
            else:
                line.margin = -100
                line.margin_value = - line.cost * line.quantity
        return res

    def action_invoice_print(self):
        super(AccountMove, self).action_invoice_print()
        if self.user_has_groups('account.group_account_invoice'):
            return self.env.ref(
                'studio_customization.factures_397dccda-ed73-4e20-9841-5aa842f63c0c').report_action(
                    self)
        else:
            return self.env.ref(
                'account.account_invoices_without_payment').report_action(self)
