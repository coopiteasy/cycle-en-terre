# © 2016 Robin Keunen, Coop IT Easy SCRL fs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    covered_surface = fields.Float(
        string='Covered Surface (m²)',
    )
    variant_sale_ok = fields.Boolean(
        string='Can be Sold (Variant)',
    )
    default_variant = fields.Boolean(
        string='Default Variant',
        compute='_compute_default_variant',
        inverse='_inverse_default_variant',
        store=True,
    )
    # todo migrate to many2many
    label = fields.Char(
        string="Label",
    )
    # todo weight unit of measure

    def _compute_default_variant(self):
        return self.default_variant

    def _inverse_default_variant(self):
        self.ensure_one()
        if self.default_variant:
            other_variants = (
                self
                .product_tmpl_id
                .product_variant_ids
                .filtered(lambda p: p.id != self.id)
            )
            for product in other_variants:
                product.default_variant = False

        return
