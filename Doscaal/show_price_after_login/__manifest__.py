# -*- coding: utf-8 -*-
#################################################################################
# Author      : CodersFort (<https://codersfort.com/>)
# Copyright(c): 2017-Present CodersFort.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://codersfort.com/>
#################################################################################

{
    "name": "Website Show Price After Login (Website Hide Price)",
    "summary": "This module allow to hide price for not logged in user in website sale, Hide product price and add to cart button in shop page and product page.",
    "version": "13.0.1",
    "description": """
        This module allow to hide price for not logged in user in website sale, Hide product price and add to cart button in shop page and product page.
        Show Price after Login
        Login to see the Price
    """,    
    "author": "CodersFort",
    "maintainer": "Ananthu Krishna",
    "license" :  "Other proprietary",
    "website": "http://www.codersfort.com",
    "images": ["images/show_price_after_login.png"],
    "category": "eCommerce",
    "depends": ["website_sale"],
    "data": [
        "views/product.xml",
        "views/res_config_settings_views.xml",                            
        "views/templates.xml",
        "wizard/price_visibility_update.xml",
    ],
    "qweb": [],
    "installable": True,
    "application": True,
    "price"                :  14,
    "currency"             :  "EUR",
    "pre_init_hook"        :  "pre_init_check",   
}