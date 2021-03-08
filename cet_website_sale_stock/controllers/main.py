# Copyright 2018 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.website_sale_product_seeds.controllers.main import (
    WebsiteSale as Base,
)

from odoo import http
from odoo.http import request

# TODO: use a config to let user configure these values
FUZZY_DEFAULT_TRESHOLD = 0.1
FUZZY_CATEGORY_TRESHOLD = 0.3


class WebsiteSale(Base):
    @http.route(
        ["/shop/product/stock_info"], type="json", website=True, auth="public"
    )
    def get_product_stock_info(self, **kwargs):
        """Give a json data structure that contains informations about
        the available stock for a product variant.
        """
        product_id = kwargs.get("id", None)
        product = request.env["product.product"].sudo().browse(product_id)
        if product:
            return {
                "id": product.id,
                "virtual_available": product.virtual_available,
                "inventory_availability": product.inventory_availability,
                "available_threshold": product.available_threshold,
                "custom_message": product.custom_message,
                "cart_qty": product.cart_qty,
            }
        else:
            return {"error": True}

    @http.route(["/shop/cart"], type="http", auth="public", website=True)
    def cart(self, access_token=None, revive="", **post):
        response = super().cart(access_token, revive, **post)
        sale_order = request.website.sale_get_order()
        sale_order._check_cart_available_threshold()
        return response

    @http.route(["/shop/checkout"], type="http", auth="public", website=True)
    def checkout(self, **post):
        response = super().checkout(**post)
        sale_order = request.website.sale_get_order()
        if sale_order._is_threshold_reached():
            return request.redirect("/shop/cart")
        return response
