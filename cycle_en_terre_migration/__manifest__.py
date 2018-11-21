{
    'name': "Cycle en Terre - Migrations",

    'summary': """
        Migration scripts for Cycle en Terre""",

    'author': "Coop IT Easy SCRL",
    'website': "https://www.coopiteasy.be",
    'license': 'AGPL-3',

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
