{
    "name": "Cycle en Terre - Custom Modifications",
    "summary": """
        Customizations for Cycle en Terre""",
    "author": "Coop IT Easy SCRL",
    "website": "https://www.coopiteasy.be",
    "license": "AGPL-3",
    "category": "Uncategorized",
    "version": "11.0.0.0.1",
    "depends": ["account", "product_seeds", "stock", "sale"],
    "data": [
        "report/report_invoice.xml",
        "report/report_stockpicking_operations.xml",
        "report/sale_report.xml",
        "views/account_invoice_views.xml",
        "views/sale_views.xml",
        "views/account_invoice_views.xml",
        "views/stock_picking_views.xml",
    ],
    "installable": True,
}
