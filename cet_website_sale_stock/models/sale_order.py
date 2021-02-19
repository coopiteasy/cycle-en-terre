# Copyright 2018 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models, api, fields
from odoo.tools.translate import _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    warning_threshold = fields.Char("Warning Threshold")

    @api.multi
    def _is_threshold_reached(self):
        for line in self.order_line:
            if line._is_threshold_reached():
                return True
        return False

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
                new_val = self._cart_update(  # todo check line.produc_id is product.product
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
        return (
            self.product_id.type == "product"
            and self.product_id.inventory_availability
            in ["always", "threshold"]
            and threshold_reached
        )

    @api.multi
    def _get_threshold_warning(self, clear=True):
        self.ensure_one()
        warn = self.warning_threshold
        if clear:
            self.warning_threshold = ""
        return warn
