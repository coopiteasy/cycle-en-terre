# Copyright 2018 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models, api, fields
from odoo.tools.translate import _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    warning_customer_type = fields.Char("Warning Customer Type")

    @api.multi
    def _is_restricted(self, customer_type_id):
        for line in self.order_line:
            if line._is_restricted(customer_type_id):
                return True
        return False

    @api.multi
    def _check_cart_customer_type(self, customer_type_id):
        if not customer_type_id.sudo().website_restrict_product:
            return
        values = {}
        restricted_products = []
        for line in self.order_line:
            if line._is_restricted(customer_type_id):
                restricted_products.append(line.product_id.name)
                self._cart_update(
                    product_id=line.product_id.id,
                    line_id=line.id,
                    add_qty=None,
                    set_qty=0,
                )
                self.warning_customer_type = _(
                    "The following products are restricted for your customer type "
                    "and have been removed from your cart: %s"
                ) % ", ".join(p for p in restricted_products)
                values["warning_customer_type"] = self.warning_customer_type
        return values

    @api.multi
    def _get_customer_type_warning(self, clear=True):
        self.ensure_one()
        warn = self.warning_customer_type
        if clear:
            self.warning_customer_type = ""
        return warn


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def _is_restricted(self, customer_type_id):
        self.ensure_one()
        return (
            self.product_id.type == "product"
            and customer_type_id not in self.product_id.customer_type_ids
        )
