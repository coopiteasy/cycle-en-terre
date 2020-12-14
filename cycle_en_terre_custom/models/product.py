from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    property_account_income_id = fields.Many2one(
        "account.account",
        company_dependent=True,
        string="Product Variant Income Account",
    )
    property_account_expense_id = fields.Many2one(
        "account.account",
        company_dependent=True,
        string="Product Variant Expense Account",
    )

    @api.multi
    def get_product_accounts(self, fiscal_pos=None):
        product_tmpl_accounts = self.product_tmpl_id.get_product_accounts(
            fiscal_pos=fiscal_pos
        )
        product_variant_accounts = self._get_product_variant_accounts()
        product_tmpl_accounts.update(
            {
                "variant_income": product_variant_accounts["variant_income"],
                "variant_expense": product_variant_accounts["variant_expense"],
            }
        )
        return product_tmpl_accounts

    @api.multi
    def _get_product_variant_accounts(self):
        return {
            "variant_income": self.property_account_income_id,
            "variant_expense": self.property_account_expense_id,
        }
