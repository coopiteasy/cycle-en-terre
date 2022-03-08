# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _


class LegalInformationCertification(models.Model):
    _name = "legal.information.certification"
    _description = 'Certification'

    name = fields.Char(string="Name", required=True)
    product_ids = fields.One2many(
        'product.template',
        inverse_name='certification_id',
    )
