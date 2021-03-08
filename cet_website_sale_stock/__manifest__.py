# Copyright 2018-2020 Coop IT Easy SCRLfs <https://coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Cycle en Terre Website Sale Stock",
    "summary": "Adaptation for Cycle en Terre to website_sale_stock",
    "version": "11.0.0.0.0",
    "category": "e-commerce",
    "website": "https://github.com/coopiteasy/cycle-en-terre/",
    "author": "Coop IT Easy SCRLfs",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website_sale_stock",
        "cet_website_sale",
    ],
    "data": [
        "views/assets.xml",
        "views/product.xml",
        "views/templates.xml",
        "views/website_sale_templates.xml",
    ],
}
