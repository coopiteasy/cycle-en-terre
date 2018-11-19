from odoo import models, fields


class SeedlingMonth(models.Model):
    _name = 'seedling.month'
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

    species = fields.Char(
        string='Species',
    )
    seedling_months = fields.Many2many(
        comodel_name='seedling.month',
        string='Seedling Month',
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
    species_information = fields.Text(
        string='Species Information',
    )
    culture_information = fields.Text(
        string='Culture Information',
    )
    recipe = fields.Html(
        string='Recipe',
    )
