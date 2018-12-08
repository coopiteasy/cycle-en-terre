# © 2016 Robin Keunen, Coop IT Easy SCRL fs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def _get_kg(self):
        return self.env['product.uom'].search([('name', '=', 'kg')])

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

    weight_unit = fields.Many2one(
        comodel_name='product.uom',
        default=_get_kg,
        domain=[('category_id.name', '=', 'Weight')],
    )
    display_weight = fields.Float(
        compute='_compute_display_weight',
        inverse='_inverse_display_weight',
        store=True,
    )

    @api.multi
    def _compute_default_variant(self):
        for product in self:
            product.default_variant = product.default_variant

    @api.multi
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

    @api.depends('weight_unit', 'weight')
    def _compute_display_weight(self):
        """Default weight is set in kg, this function computes the weight
        displayed with the product unit """
        for product in self:
            unit_factor = product.weight_unit.factor
            product.display_weight = product.weight * unit_factor

    @api.depends('weight_unit', 'weight', 'display_weight')
    def _inverse_display_weight(self):
        """Default weight is set in kg, this function computes the weight
        displayed with the product unit """
        for product in self:
            # product.display_weight = product.display_weight
            unit_factor = product.weight_unit.factor
            product.weight = product.display_weight / unit_factor
