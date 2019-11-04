# © 2016 Robin Keunen, Coop IT Easy SCRL fs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from odoo import models


def get_attribute(attribute):
    key = attribute.attribute_id.name
    value = attribute.value_ids.mapped("name")
    return key, value


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def get_seedling_months(self):
        seedling_months = self.env["seed.seedling.month"].search([])
        month_map = {
            "Janvier": seedling_months.filtered(lambda m: m.name == "January"),
            "Février": seedling_months.filtered(
                lambda m: m.name == "February"
            ),  # noqa
            "Mars": seedling_months.filtered(lambda m: m.name == "March"),
            "Avril": seedling_months.filtered(lambda m: m.name == "April"),
            "Mai": seedling_months.filtered(lambda m: m.name == "May"),
            "Juin": seedling_months.filtered(lambda m: m.name == "June"),
            "Juillet": seedling_months.filtered(lambda m: m.name == "July"),
            "Aout": seedling_months.filtered(lambda m: m.name == "August"),
            "Août": seedling_months.filtered(lambda m: m.name == "August"),
            "Septembre": seedling_months.filtered(
                lambda m: m.name == "September"
            ),  # noqa
            "Octobre": seedling_months.filtered(lambda m: m.name == "October"),
            "Novembre": seedling_months.filtered(
                lambda m: m.name == "November"
            ),  # noqa
            "Décembre": seedling_months.filtered(
                lambda m: m.name == "December"
            ),  # noqa
        }
        return month_map

    def migrate_variants_to_template(self):
        """Migration 1:
            - set is_species to true
            - migrate species, latin_name, seedling_month_data"""
        templates = self.search([])
        seedling_months = self.get_seedling_months()

        for template in templates:
            assert len(template.product_variant_ids) == 1
            attribute_lines = template.product_variant_ids.attribute_line_ids
            attributes = {k: v for k, v in map(get_attribute, attribute_lines)}

            if "Espèce" not in attributes:
                # assuming product is not a species if the attribute is not set
                continue

            species = attributes["Espèce"][0]
            latin_name = attributes.get("Nom latin", None)
            template_months = [
                seedling_months[m] for m in attributes.get("Mois de semis", [])
            ]  # noqa

            template.write(
                {
                    "is_species": True,
                    "species": species,
                    "latin_name": latin_name[0] if latin_name else None,
                    "seedling_month_ids": [
                        (6, 0, [m.id for m in template_months])
                    ],
                }
            )

    def unlink_product_variant_deprecated_attribute(self):
        """Migration 2:
            - unlink attributes values from product.product
            - unlink attributes lines from product.template"""
        templates = self.search([])
        logger = logging.getLogger(__name__)
        logger.info("run cron unlink_product_variant_deprecated_attribute")

        for template in templates:
            logger.info(template.name)
            variants = template.product_variant_ids

            for variant in variants:
                attribute_values = variant.mapped(
                    "attribute_value_ids"
                ).filtered(lambda av: not av.attribute_id.is_package)
                logger.info(attribute_values.mapped("name"))
                variant.attribute_value_ids = [
                    (3, av.id, 0) for av in attribute_values
                ]

            attribute_lines = template.attribute_line_ids.filtered(
                lambda al: not al.attribute_id.is_package
            )
            template.attribute_line_ids = [
                (3, al.id, 0) for al in attribute_lines
            ]

            # self.env.cr.commit()

    def delete_attributes(self):
        """
        Migration 3;
            - unlink all attribute values
            - unlink all attributes

        If attribute lines remain, use:
        ```
            delete from product_attribute_line
            where attribute_id != <package id>
        ```
        """
        logger = logging.getLogger(__name__)
        values = (
            self.env["product.attribute.value"]
            .search([("attribute_id.is_package", "=", False)])
            .filtered(lambda v: not v.attribute_id.is_package)
        )
        logger.info("unlink %s" % values.mapped("name"))
        values.unlink()

        attributes = (
            self.env["product.attribute"]
            .search([("is_package", "=", False)])
            .filtered(lambda a: not a.is_package)
        )
        logger.info("unlink %s " % attributes.mapped("name"))
        attributes.unlink()

        return
