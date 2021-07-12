# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class HrExpense(models.Model):

    _inherit = "hr.expense"


    @api.model
    def _get_employee_id_domain(self):
        res = super(HrExpense, self)._get_employee_id_domain()
        if res == [('id', '=', 0)]: # Nothing accepted by domain, by default
            res = [('user_id', '=', self.env.user.id)]
        return res
