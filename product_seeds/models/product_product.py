# © 2016 Robin Keunen, Coop IT Easy SCRL fs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    covered_surface = fields.Float(
        string='Covered Surface (m²)',
    )
    variant_sale_ok = fields.Boolean(
        string='Can be Sold (Variant)',
    )
    # todo set other variants default to false (on change)
    default_variant = fields.Boolean(
        string='Default Variant',
    )
    # todo migrate to many2many
    label = fields.Char(
        string="Label",
    )
    # todo weight unit of measure
