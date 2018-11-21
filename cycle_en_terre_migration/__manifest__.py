# -*- coding: utf-8 -*-
# © 2016 Robin Keunen, Coop IT Easy SCRL fs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# -*- coding: utf-8 -*-
{
    'name': "Cycle en Terre - Migrations",

    'summary': """
        Migration scripts for Cycle en Terre""",

    'author': "Coop IT Easy SCRL",
    'website': "https://www.coopiteasy.be",

    'category': 'Warehouse Management',
    'version': '11.0.0.0.1',

    'depends': [
        'product_seeds',
    ],

    'data': [
        'data/cron.xml',
    ],
    'installable': True,
    'test': [],
}
