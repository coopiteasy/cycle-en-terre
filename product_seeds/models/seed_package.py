# © 2016 Robin Keunen, Coop IT Easy SCRL fs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProductAttribute(models.Model):
    _inherit = "product.attribute"
    is_package = fields.Boolean()


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    @api.model
    def create(self, vals):
        attribute = super(ProductAttributeValue, self).create(vals)

        if (
            attribute.attribute_id.is_package
            and "seed_package" not in self._context
        ):
            (
                self.env["seed.package"].create(
                    {"attribute_value_id": attribute.id}
                )
            )

        return attribute


class SeedPackage(models.Model):
    _name = "seed.package"
    _inherits = {"product.attribute.value": "attribute_value_id"}

    @api.model
    def create(self, vals):
        package_attribute = (
            self.env["product.attribute"]
            .search([("is_package", "=", True)])
            .ids
        )

        if len(package_attribute) == 0:
            raise ValidationError(_("No product attributes is set as package"))

        if len(package_attribute) > 1:
            raise ValidationError(
                _("Several product attributes are set as packages")
            )  # noqa

        vals["attribute_id"] = package_attribute.pop()

        package = super(
            SeedPackage, self.with_context(seed_package=True)
        ).create(vals)
        return package

    @api.constrains("attribute_value_id")
    def _check_attribute_value(self):
        for package in self:
            if not package.attribute_id.is_package:
                raise ValidationError(
                    _('Attribute must be "package" (is_package == True)')
                )  # noqa
