# Copyright 2020 Coop IT Easy SCRLfs <http://coopiteasy.be>
#   Rémy Taymans <remy@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models


class ResPartnerCategory(models.Model):
    _name = "res.partner.category"
    _inherit = "res.partner.category"

    website_restrict_product = fields.Boolean(
        string="Restrict Product on E-commerce",
    )
    website_product_ids = fields.Many2many(
        comodel_name="product.product",
        string="Product",
        help=(
            "Choose product that can be viewed on e-commerce by users "
            "that belongs to this category."
        )
    )
