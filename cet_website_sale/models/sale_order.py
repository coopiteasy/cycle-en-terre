# Copyright 2018 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models, api, fields
from odoo.tools.translate import _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    warning_customer_type = fields.Char("Warning Customer Type")
    warning_threshold = fields.Char("Warning Threshold")

    @api.multi
    def _is_threshold_reached(self):
        for line in self.order_line:
            if line._is_threshold_reached():
                return True
        return False

    @api.multi
    def _check_cart_customer_type(self, customer_type_id):
        if not customer_type_id.sudo().website_restrict_product:
            return
        values = {}
        restricted_products = []
        for line in self.order_line:
            if (
                line.product_id.type == "product"
                and customer_type_id not in line.product_id.customer_type_ids
            ):
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
    def _check_cart_available_threshold(self):
        values = {}
        updated_products = []
        for line in self.order_line:
            if line._is_threshold_reached():
                updated_products.append(line.product_id.name)
                max_qty = (
                    line.product_id.virtual_available
                    - line.product_id.available_threshold
                )
                new_val = self._cart_update(
                    product_id=line.product_id.id,
                    line_id=line.id,
                    add_qty=None,
                    set_qty=max_qty,
                )
                # Make sure line still exists, it may have been deleted in self._cart_update
                # because set_qty can be <= 0
                if line.exists() and new_val["quantity"]:
                    line.warning_threshold = _(
                        "Only %s is available for product %s"
                        % (new_val["quantity"], line.product_id.name)
                    )
                self.warning_threshold = _(
                    "The following products became unavailable "
                    "and have been updated: %s"
                ) % ", ".join(p for p in updated_products)
                values["warning_threshold"] = self.warning_threshold
        return values

    @api.multi
    def _get_customer_type_warning(self, clear=True):
        self.ensure_one()
        warn = self.warning_customer_type
        if clear:
            self.warning_customer_type = ""
        return warn

    @api.multi
    def _get_threshold_warning(self, clear=True):
        self.ensure_one()
        warn = self.warning_threshold
        if clear:
            self.warning_threshold = ""
        return warn


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    warning_threshold = fields.Char("Warning Threshold")

    @api.multi
    def _is_threshold_reached(self):
        self.ensure_one()
        threshold_reached = (
            self.product_id.virtual_available - self.product_id.cart_qty
        ) < self.product_id.available_threshold
        if (
            self.product_id.type == "product"
            and self.product_id.inventory_availability
            in ["always", "threshold"]
            and threshold_reached
        ):
            return True
        return False

    @api.multi
    def _get_threshold_warning(self, clear=True):
        self.ensure_one()
        warn = self.warning_threshold
        if clear:
            self.warning_threshold = ""
        return warn
