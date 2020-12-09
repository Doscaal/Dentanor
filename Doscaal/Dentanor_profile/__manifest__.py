# copyright Doscaal 2019
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
# -*- coding: utf-8 -*-

{
    'name': 'Dentanor Profile',
    'version': '13.0.1.2',
    'category': 'Custom',
    'description': """Profile for Dentanor""",
    'author': 'Doscaal',
    'website': 'http://www.doscaal.fr/',
    'depends': [
        # 'stock_barcodes',
        'sale',
        'sale_margin',
        'account_followup',
    ],
    'images': [],
    'data': [
        'views/account_move.xml',
        'views/res_partner.xml',
        'views/sale_order.xml',
    ],
    'test': [],
    'installable': True,
    'active': True,
    'license': 'AGPL-3',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
