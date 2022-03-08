# © 2016 Robin Keunen, Coop IT Easy SCRL fs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _get_g(self):
        g = self.env["product.uom"].search([("name", "=", "g")])

        if not g:
            raise ValidationError(_("Missing reference weight g"))
        elif len(g) == 1:
            return g
        else:
            raise ValidationError(_("Several units named g"))

    covered_surface = fields.Float(string="Covered Surface (m²)")
    variant_sale_ok = fields.Boolean(string="Can be Sold (Variant)")
    default_variant = fields.Boolean(
        string="Default Variant",
        compute="_compute_default_variant",
        inverse="_inverse_default_variant",
        store=True,
    )
    # todo migrate to many2many
    label = fields.Char(string="Label", translate=True)

    weight_unit = fields.Many2one(
        string="Weight Unit",
        comodel_name="product.uom",
        default=_get_g,
        # domain=<weight category>, # todo
    )
    package_weight = fields.Float(
        string="Package Weight",
        compute="_compute_package_weight",
        inverse="_inverse_package_weight",
        store=True,
        help="Total package weight (seed and container), layer over weight "
        "field.",
    )
    seed_weight = fields.Float(string="Seed Weight", help="Seed Weight")
    max_seed_weight = fields.Float(string="Maximum Seed Weight", help="Maximum not to be exceeded during bagging.")
    packing_method_id = fields.Many2one(
        comodel_name="product.packing.method",
        string="Packing Method"
    )
    theoretical_packing_time = fields.Float(string="Theoretical Packing Time")
    theoretical_adjustment_time = fields.Float(string="Theoretical Adjustment Time")
    legal_mention = fields.Text(string="Legal Mention")

    @api.multi
    def _compute_default_variant(self):
        for product in self:
            product.default_variant = product.default_variant

    @api.multi
    def _inverse_default_variant(self):
        self.ensure_one()
        if self.default_variant:
            other_variants = self.product_tmpl_id.product_variant_ids.filtered(
                lambda p: p.id != self.id
            )
            for product in other_variants:
                product.default_variant = False

        return

    @api.depends("weight_unit", "weight")
    def _compute_package_weight(self):
        """Default weight is set in kg, this function computes the weight
        displayed with the product unit """
        for product in self:
            unit_factor = product.weight_unit.factor
            product.package_weight = product.weight * unit_factor

    @api.depends("weight_unit", "weight", "package_weight")
    def _inverse_package_weight(self):
        """Default weight is set in kg, this function computes the weight
        displayed with the product unit """
        for product in self:
            unit_factor = product.weight_unit.factor
            product.weight = product.package_weight / unit_factor
