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
        "website_sale_category_megamenu",
    ],
    "data": [
        "views/category_megamenu_templates.xml",
        "views/assets.xml",
    ],
}
