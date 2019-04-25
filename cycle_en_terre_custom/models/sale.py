
from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    label = fields.Char(
        string='Label',
        default=lambda self: self.product_id.label,
    )
    seed_weight = fields.Float(
        string='Seed Weight',
        default=lambda self: self.product_id.seed_weight,
    )
    weight_unit = fields.Many2one(
        comodel_name='product.uom',
        string='Weight Unit',
        default=lambda self: self.product_id.weight_unit,
    )

    @api.onchange('product_id')
    def onchange_product_id(self):
        self.label = self.product_id.label
        self.seed_weight = self.product_id.seed_weight
        self.weight_unit = self.product_id.weight_unit
