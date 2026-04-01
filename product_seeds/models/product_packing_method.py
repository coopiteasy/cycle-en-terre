# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _


class ProductProduct(models.Model):
    _name = "product.packing.method"
    _description = "Packing Method"

    name = fields.Char(string="Name", required=True)
    product_ids = fields.One2many(
        'product.product',
        inverse_name='packing_method_id',
    )

