from odoo import models, fields


class SeedlingMonth(models.Model):
    _name = 'seed.seedling.month'
    _order = 'sequence'

    sequence = fields.Integer(
        string='Sequence',
        required=True,
        readonly=True,
    )
    name = fields.Char(
        string="Name",
        required=True,
        readonly=True,
    )


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_species = fields.Boolean(
        string='Is Species',
    )
    species = fields.Char(
        string='Species',
    )
    seedling_months = fields.Many2many(
        comodel_name='seed.seedling.month',
        string='Seedling Month',
    )
    produced_in_house = fields.Boolean(
        string='Produced in House',
    )
    latin_name = fields.Char(
        string='Latin Name',
    )
    emergence = fields.Integer(
        string='Emergence (days)',
    )
    density = fields.Float(
        string='Density (g/10 m²)',
    )
    germination = fields.Float(
        string='Germination (years)'
    )
    thousand_grain_weight = fields.Float(
        string='Thousand Grain Weight (g)',
    )
    species_information = fields.Text(
        string='Species Information',
    )
    culture_information = fields.Text(
        string='Culture Information',
    )
    recipe = fields.Html(
        string='Recipe',
    )
    beemeadow = fields.Boolean(
        string='Beemeadow',
    )
    spacing_between_lines = fields.Char(
        string='Spacing Between Lines',
    )
    spacing_within_line = fields.Char(
        string='Spacing Within Line',
    )
    light_requirements = fields.Char(
        string='Light Requirements',
    )
    comment = fields.Text(
        string='Comment',
    )
