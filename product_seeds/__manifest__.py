{
    "name": "Seeds - Products",
    "summary": """
        Customization of product_template to manage:
        - seed production
        - variety
        - variant
    """,
    "author": "Coop IT Easy SCRL",
    "website": "https://www.coopiteasy.be",
    "license": "AGPL-3",
    "category": "Warehouse Management",
    "version": "11.0.0.1.1",
    "depends": ["product", "sale", "stock", "website_sale"],
    "data": [
        "data/data.xml",
        "views/product_product.xml",
        "views/product_template.xml",
        "views/seed_package.xml",
        "views/seedling_months.xml",
        "views/legal_information_menu_item.xml",
        "views/legal_information_certification.xml",
        "views/legal_information_mention.xml",
        "views/legal_information_variety_right.xml",
        "security/ir.model.access.csv",
    ],
    "demo": ["demo/demo.xml"],
    "installable": True,
}
