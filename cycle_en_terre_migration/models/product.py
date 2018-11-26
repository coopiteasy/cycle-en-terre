# © 2016 Robin Keunen, Coop IT Easy SCRL fs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models


def get_attribute(attribute):
    key = attribute.attribute_id.name
    value = attribute.value_ids.mapped('name')
    return key, value


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def get_seedling_months(self):
        seedling_months = self.env['seed.seedling.month'].search([])
        month_map = {
            'Janvier': seedling_months.filtered(lambda m: m.name == 'January'),
            'Février': seedling_months.filtered(lambda m: m.name == 'February'),  # noqa
            'Mars': seedling_months.filtered(lambda m: m.name == 'March'),
            'Avril': seedling_months.filtered(lambda m: m.name == 'April'),
            'Mai': seedling_months.filtered(lambda m: m.name == 'May'),
            'Juin': seedling_months.filtered(lambda m: m.name == 'June'),
            'Juillet': seedling_months.filtered(lambda m: m.name == 'July'),
            'Aout': seedling_months.filtered(lambda m: m.name == 'August'),
            'Août': seedling_months.filtered(lambda m: m.name == 'August'),
            'Septembre': seedling_months.filtered(lambda m: m.name == 'September'),  # noqa
            'Octobre': seedling_months.filtered(lambda m: m.name == 'October'),
            'Novembre': seedling_months.filtered(lambda m: m.name == 'November'),  # noqa
            'Décembre': seedling_months.filtered(lambda m: m.name == 'December'),  # noqa
        }
        return month_map

    def migrate_variants_to_template(self):
        """Migration 1"""
        templates = self.search([])
        seedling_months = self.get_seedling_months()

        for template in templates:
            assert len(template.product_variant_ids) == 1
            attribute_lines = template.product_variant_ids.attribute_line_ids
            attributes = {k: v for k, v in map(get_attribute, attribute_lines)}

            if 'Espèce' not in attributes:
                # assuming product is not a species if the attribute is not set
                continue

            species = attributes['Espèce'][0]
            latin_name = attributes.get('Nom latin', None)
            template_months = [seedling_months[m] for m in attributes.get('Mois de semis', [])]  # noqa

            template.write({
                'is_species': True,
                'species': species,
                'latin_name': latin_name[0] if latin_name else None,
                'seedling_months': [(6, 0, [m.id for m in template_months])],
            })
