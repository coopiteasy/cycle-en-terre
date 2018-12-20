from odoo import models, fields


class SeedlingMonth(models.Model):
    _name = 'seed.seedling.month'
    _order = 'sequence'

    sequence = fields.Integer(
        string='Sequence',
        required=True,
    )
    name = fields.Char(
        string="Name",
        required=True,
        translate=True,
    )


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_species = fields.Boolean(
        string='Is Species',
    )
    species = fields.Char(
        string='Species',
    )
    seedling_month_ids = fields.Many2many(
        comodel_name='seed.seedling.month',
        string='Seedling Months',
        relation='product_template_seed_seedling_month_rel',
    )
    flowering_month_ids = fields.Many2many(
        comodel_name='seed.seedling.month',
        string='Flowering Months',
        relation='product_template_flowering_months_rel',
    )
    harvest_month_ids = fields.Many2many(
        comodel_name='seed.seedling.month',
        string='Harvest Months',
        relation='product_template_harvest_months_rel',
    )
    sowing_indoors_month_ids = fields.Many2many(
        comodel_name='seed.seedling.month',
        string='Sowing Indoors Months',
        relation='product_template_sowing_indoors_months_rel',
    )
    sowing_outoors_month_ids = fields.Many2many(
        comodel_name='seed.seedling.month',
        string='Sowing Outdoors Months',
        relation='product_template_sowing_outoors_months_rel',
    )
    pot_planting_month_ids = fields.Many2many(
        comodel_name='seed.seedling.month',
        string='Pot Planting Months',
        relation='product_template_pot_planting_months_rel',
    )
    produced_in_house = fields.Boolean(
        string='Produced in House',
    )
    latin_name = fields.Char(
        string='Latin Name',
    )
    emergence = fields.Char(
        string='Emergence',
        tanslate=True,
    )
    density = fields.Float(
        string='Density (g/10 m²)',
    )
    germination = fields.Char(
        string='Germination',
        translate=True,
    )
    thousand_grain_weight = fields.Float(
        string='Thousand Grain Weight (g)',
    )
    species_information = fields.Text(
        string='Species Information',
        translate=True,
    )
    culture_information = fields.Text(
        string='Culture Information',
        translate=True,
    )
    recipe = fields.Html(
        string='Recipe',
        translate=True,
    )
    beemeadow = fields.Boolean(
        string='Beemeadow',
    )
    spacing_between_lines = fields.Char(
        string='Spacing Between Lines',
        translate=True,
    )
    spacing_within_line = fields.Char(
        string='Spacing Within Line',
        translate=True,
    )
    light_requirements = fields.Char(
        string='Light Requirements',
        translate=True,
    )
    comment = fields.Text(
        string='Comment',
        translate=True,
    )
