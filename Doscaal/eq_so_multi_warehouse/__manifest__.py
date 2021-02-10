# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 EquickERP
#
##############################################################################

{
    'name': "Sale Multi Warehouse",
    'version': '13.0.1.0',
    'category': 'Sales',
    'author': 'Equick ERP',
    'summary': """ sale order multi warehouse | Sales multi warehouse | warehouse on sale order line | SO multi warehouse | sale order warehouse | multi picking | multi transfer | so multi picking | sale picking by warehouse.""",
    'description': """
        Sales Multi warehouse
        =======================
        * Allow user to select different warehouse on Sales order line.
        * Generate Delivery orders based on the warehouse selected.
        * User can see the warehouse on Pdf Report, Sales analysis report, Customer portal view.
    """,
    'license': 'OPL-1',
    'depends': ['sale_management', 'sale_stock'],
    'price': 14,
    'currency': 'EUR',
    'website': "",
    'data': [
        'views/sale_view.xml',
        'views/sale_report_template.xml'
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: