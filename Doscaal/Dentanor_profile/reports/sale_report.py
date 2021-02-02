# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleReport(models.Model):
    _inherit = "sale.report"

    supplier_id = fields.Many2one(comodel_name='res.partner',
                                  string='Fournisseur')

    @api.model
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        res = super(SaleReport, self)._query(with_clause, fields,
                                             groupby, from_clause)
        res = res.replace(
            's.id as order_id',
            's.id as order_id, (select name from product_product pp left join product_supplierinfo ps on ps.product_tmpl_id = pp.product_tmpl_id where pp.id = l.product_id order by sequence limit 1) as supplier_id')
        return res
