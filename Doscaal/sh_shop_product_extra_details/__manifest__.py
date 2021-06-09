# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

{
    'name': 'Shop Product Extra Details',

    'author': 'Softhealer Technologies',

    'website': 'https://www.softhealer.com',

    "support": "support@softhealer.com",

    'version': '13.0.1',

    'category': 'Website',

    "license": "OPL-1",

    'summary': 'Product Barcode Number At Shop Page, Product Unit Of Measure Website, Product Internal Reference Number At Website, Product UOM On Web, Product Extra Details Shop, Product More Details Website Odoo ',

    'description': """Currently, odoo not provide to show extra product details on the shop page. This module allows you to add details in the product at the website like barcode number, unit of measure & internal reference number.""",

    'depends': ['website_sale'],

    'data': [
            'views/res_config_settings.xml',
            'views/shop_product.xml',
    ],
    "images": ["static/description/background.png", ],
    'auto_install': False,
    'installable': True,
    'application': True,
    "price": 25,
    "currency": "EUR"
}
