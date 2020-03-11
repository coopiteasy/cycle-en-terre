# Copyright 2020 Coop IT Easy SCRLfs <http://coopiteasy.be>
#   Rémy Taymans <remy@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    website_restrict_product = fields.Boolean(
        string="Restrict Product on E-commerce",
        compute="_compute_website_restrict_product"
    )
    website_product_ids = fields.Many2many(
        comodel_name="product.product",
        string="Product",
        compute="_compute_website_product_ids",
        help=(
            "Choose product that can be viewed on e-commerce by users "
            "that belongs to this category."
        )
    )

    @api.depends("category_id")
    def _compute_website_restrict_product(self):
        """
        Set website_restrict_product to True if at least one category
        has the flag website_restrict_product set.
        """
        for partner in self:
            for categ in partner.category_id:
                if categ.website_restrict_product:
                    partner.website_restrict_product = True
                    break

    @api.depends("category_id")
    def _compute_website_product_ids(self):
        """
        Return the list of product that can be seen on the e-commerce by
        the partner if connected.
        Aggregate all products from each category assigned to the
        partner and that has website_restrict_product set on.
        """
        for partner in self:
            products = self.env["product.product"]
            for categ in partner.category_id:
                if categ.website_restrict_product:
                    products |= categ.website_product_ids
            partner.website_product_ids = products
