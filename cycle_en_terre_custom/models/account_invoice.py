from odoo import fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    label = fields.Char(
        string='Label',
        related='product_id.label',
    )
    seed_weight = fields.Float(
        string='Seed Weight',
        related='product_id.seed_weight',
    )
    weight_unit = fields.Many2one(
        string='Weight Unit',
        related='product_id.weight_unit',
    )
