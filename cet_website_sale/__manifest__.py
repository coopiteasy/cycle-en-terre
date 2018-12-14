# Copyright 2018 Coop IT Easy SCRLfs <https://coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Cycle en Terre Website Sale",
    "summary": "Adaptation for Cycle en Terre to the e-Commerce",
    "version": "11.0.1.0.0",
    "category": "e-commerce",
    "website": "https://github.com/coopiteasy/cycle-en-terre/",
    "author": "Coop IT Easy SCRLfs",
    "license": "AGPL-3",
    "application": False,
    'installable': True,
    "depends": [
        "website_sale",
        "website_sale_options",
        "website_sale_delivery",
        "website_sale_category_megamenu",
        "website_sale_category_breadcrumb",
        "website_sale_product_seeds",
        "product_seeds",
    ],
    "data": [
        "views/templates.xml",
        "views/website_sale_templates.xml",
        "views/website_sale_options_templates.xml",
        "views/category_megamenu_templates.xml",
        "views/assets.xml",
    ],
}
