# copyright Doscaal 2021
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
        'stock_barcodes',
        'sale',
        'sale_margin',
        'account_followup',
        'payment_payzen',
        'show_price_after_login',
        'sale_product_configurator',
        'l10n_fr_intrastat_product',
        'purchase',
        'industry_fsm_stock',
        'industry_fsm_report',
    ],
    'images': [],
    'data': [
        'security/ir.model.access.csv',
        'security/sale_security.xml',
        'security/account_security.xml',
        'views/account_move_line.xml',
        'views/account_move.xml',
        'views/res_partner.xml',
        'views/sale_order.xml',
        'views/product_template.xml',
        'views/barcode_expression.xml',
        'data/ir_ui_menu.xml',
        'wizard/stock_barcodes_read_picking.xml',
        'views/product_supplierinfo.xml',
        'data/project_worksheet_template_data.xml',
        'views/dentanor_project_worksheet_template.xml',
        'reports/dentanor_project_worksheet_template.xml',
    ],
    'test': [],
    'installable': True,
    'active': True,
    'license': 'AGPL-3',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
