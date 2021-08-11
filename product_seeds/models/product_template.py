from odoo import models, fields
from odoo.tools.translate import html_translate



class SeedlingMonth(models.Model):
    _name = "seed.seedling.month"
    _order = "sequence"

    sequence = fields.Integer(string="Sequence", required=True)
    name = fields.Char(string="Name", required=True, translate=True)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_species = fields.Boolean(string="Is Species")
    species = fields.Char(string="Species")
    seedling_month_ids = fields.Many2many(
        comodel_name="seed.seedling.month",
        string="Seedling Months",
        relation="product_template_seed_seedling_month_rel",
    )
    flowering_month_ids = fields.Many2many(
        comodel_name="seed.seedling.month",
        string="Flowering Months",
        relation="product_template_flowering_months_rel",
    )
    harvest_month_ids = fields.Many2many(
        comodel_name="seed.seedling.month",
        string="Harvest Months",
        relation="product_template_harvest_months_rel",
    )
    sowing_indoors_month_ids = fields.Many2many(
        comodel_name="seed.seedling.month",
        string="Sowing Indoors Months",
        relation="product_template_sowing_indoors_months_rel",
    )
    sowing_outoors_month_ids = fields.Many2many(
        comodel_name="seed.seedling.month",
        string="Sowing Outdoors Months",
        relation="product_template_sowing_outoors_months_rel",
    )
    pot_planting_month_ids = fields.Many2many(
        comodel_name="seed.seedling.month",
        string="Pot Planting Months",
        relation="product_template_pot_planting_months_rel",
    )
    produced_in_house = fields.Boolean(string="Produced in House")
    latin_name = fields.Char(string="Latin Name")
    emergence = fields.Char(string="Emergence", translate=True)
    density = fields.Float(string="Density (g/10 m²)")
    min_seeding_density = fields.Float(string="Min. Seeding Density (g/10 m²)")
    max_seeding_density = fields.Float(string="Max. Seeding Density (g/10 m²)")
    selected_seeding_density = fields.Float(
        string="Selected Seeding Density",
        related="max_seeding_density",
        readonly=True
    )
    linear_seeding_density = fields.Float(string="Linear Seeding Density (g/m²)")
    plants_nb = fields.Float(
        string="Number of plants per m²",
        digits=(10,2),
        help="Number of plants per square meter"

    )
    germination = fields.Char(string="Germination", translate=True)
    thousand_grain_weight = fields.Float(string="Thousand Grain Weight (g)")
    thousand_plants_gram = fields.Float(
        string="Thousand Plants Gram #",
        digits=(10,2),
        help="Number of grams to have one thousand plants"
    )
    website_species_information = fields.Html(
        string="Website Species Information", translate=html_translate,
        help="Information to be displayed on the website and in the annual catalog"
    )
    website_culture_information = fields.Html(
        string="Website Culture Information", translate=html_translate,
        help="Information to be displayed on the website and in the annual catalog"
    )
    recipe = fields.Html(string="Recipe", translate=True)
    beemeadow = fields.Boolean(string="Beemeadow")
    spacing_between_lines = fields.Char(
        string="Spacing Between Lines", translate=True
    )
    spacing_within_line = fields.Char(
        string="Spacing Within Line", translate=True
    )
    spacing_between_plants = fields.Float(
        string="Plant spacing (m²)",
        digits=(10,2),
        help="Spacing between plants per square meter"
    )
    light_requirements = fields.Char(
        string="Light Requirements", translate=True
    )
    comment = fields.Text(string="Comment", translate=True)
    packet_species_information = fields.Char(
        string="Packet Species Information",
        size=150,
        translate=True,
        help="This information is printed on packets. Max. 150 characters."
    )
    packet_culture_information = fields.Char(
        string="Packet Culture Information",
        size=293,
        translate=True,
        help="This information is printed on packets. Max. 293 characters."
    )
    plant_passport_needed = fields.Boolean(
        string="Plant Passport Needed?"
    )
    plant_passport_type = fields.Selection([
        ('leguminous', 'Leguminous'),
        ('ornamental', 'Ornamental')],
        string='Plant Passport Type'
    )
    sale_years_number = fields.Integer(
        string="Sale Years Number",
        help="This information is useful to compute the sell-by date (SBD) printed on packets"
    )
