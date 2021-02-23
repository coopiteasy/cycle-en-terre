# Copyright 2021+ Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    #  make sure we can tell template from variant fields in forms
    inventory_availability = fields.Selection(
        string="Inventory Availability Template"
    )
    available_threshold = fields.Float(
        string="Availability Threshold Template"
    )
    custom_message = fields.Text(string="Custom Message Template")


class ProductProduct(models.Model):
    _inherit = "product.product"

    inventory_availability = fields.Selection(
        [
            ("never", "Sell regardless of inventory"),
            (
                "always",
                "Show inventory on website and prevent sales if not enough stock",
            ),
            (
                "threshold",
                "Show inventory below a threshold and prevent sales if not enough stock",
            ),
            ("custom", "Show product-specific notifications"),
        ],
        string="Inventory Availability Variant",
        help="Adds an inventory availability status on the web product page.",
        default="never",
    )
    available_threshold = fields.Float(
        string="Availability Threshold Variant", default=5.0
    )
    custom_message = fields.Text(string="Custom Message Variant", default="")
