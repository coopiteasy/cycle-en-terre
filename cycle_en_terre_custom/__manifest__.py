{
    'name': "Cycle en Terre - Custom Modifications",

    'summary': """
        Customizations for Cycle en Terre""",

    'author': "Coop IT Easy SCRL",
    'website': "https://www.coopiteasy.be",
    'license': 'AGPL-3',

    'category': 'Uncategorized',
    'version': '11.0.0.0.1',

    'depends': [
        'stock',
        'sale',
    ],

    'data': [
        'report/report_stockpicking_operations.xml',
        'report/sale_report.xml',
    ],
    'installable': True,
}
