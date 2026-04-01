# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _


class LegalInformationVarietyRight(models.Model):
    _name = "legal.information.variety.right"
    _description = 'Variety Right'

    name = fields.Char(string="Name", required=True)
    product_ids = fields.One2many(
        'product.template',
        inverse_name='variety_right_id',
    )
