from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    label = fields.Char(string="Label", related="product_id.label")
    seed_weight = fields.Float(
        string="Seed Weight", related="product_id.seed_weight"
    )
    weight_unit = fields.Many2one(
        string="Weight Unit", related="product_id.weight_unit"
    )

    def get_invoice_line_account(self, type, product, fpos, company):
        accounts = product.get_product_accounts(fiscal_pos=fpos)
        if accounts['variant_income'] or accounts['variant_expense']:
            if type in ('out_invoice', 'out_refund'):
                return accounts['variant_income']
            return accounts['variant_expense']
        return super(AccountInvoiceLine, self).get_invoice_line_account(type, product, fpos, company)
