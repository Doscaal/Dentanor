# copyright Doscaal 2020
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('Peuplement des account move avec les couts')


def migrate(cr, v):

    cr.execute("""UPDATE account_move_line aml
               SET cost = (
                    SELECT
                        avg(purchase_price)
                    FROM sale_order_line sol
                    WHERE id in (
                        SELECT order_line_id
                        FROM sale_order_line_invoice_rel solir
                        WHERE solir.invoice_line_id = aml.id));""")
    cr.execute("""UPDATE account_move_line aml
               SET cost = (
                    SELECT
                        value_float
                    FROM ir_property ip
                    WHERE ip.name = 'standard_price'
                        AND ip.res_id = 'product.product,' || aml.product_id
                        AND company_id = 1)
               WHERE aml.id not in (
                    SELECT
                        invoice_line_id
                    FROM sale_order_line_invoice_rel );""")
    cr.execute("""UPDATE account_move_line aml
               SET margin = (1 - aml.cost / (aml.price_subtotal /
                    aml.quantity)) * 100
               WHERE aml.price_subtotal <> 0;""")
    cr.execute("""UPDATE account_move_line aml
               SET margin = -100
               WHERE aml.price_subtotal = 0;""")
    cr.execute("""UPDATE account_move_line aml
               SET margin_value = aml.price_subtotal - (
                    aml.cost * aml.quantity);""")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
