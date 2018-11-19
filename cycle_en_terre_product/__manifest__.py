{
    'name': "Cycle en Terre - Products",

    'summary': """
        Customization of product_template for Cycle en Terre""",

    'author': "Coop IT Easy SCRL",
    'website': "https://www.coopiteasy.be",
    'license': 'AGPL-3',

    'category': 'Uncategorized',
    'version': '11.0.0.0.1',

    'depends': [
        'product'
    ],

    'data': [
        'data/data.xml',
        'views/product_template.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
}
