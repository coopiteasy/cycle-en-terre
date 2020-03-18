# Copyright 2018 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.http import request
from odoo.osv import expression
from odoo.addons.website_sale.controllers.main import PPG
from odoo.addons.website_sale_product_seeds.controllers.main import (
    WebsiteSale as Base,
)

# TODO: use a config to let user configure these values
FUZZY_DEFAULT_TRESHOLD = 0.1
FUZZY_CATEGORY_TRESHOLD = 0.3


class WebsiteSale(Base):
    def _get_search_domain(self, search, category, attrib_values):
        """Extend the search to use fuzzy search.
        And search also in the:
            - categories
            - latin name (see product_seeds)
        """
        domain = super()._get_search_domain(search, category, attrib_values)
        # Remove sale product domain from domain
        sale_domain = request.website.sale_product_domain()
        for domain_elem, sale_domain_elem in zip(domain, sale_domain):
            if domain_elem == sale_domain_elem:
                domain.remove(domain_elem)
        # Use '%' in place of 'ilike' for name search
        for i, v in enumerate(domain):
            if (
                isinstance(v, tuple)
                and len(v) == 3
                and (v[0] == "name" and v[1] == "ilike")
            ):
                domain[i] = (v[0], "%", v[2])
        # Normalize domain
        domain = expression.normalize_domain(domain)
        # Add new field in search domain
        if search:
            for word in search.split(" "):
                # Latin name
                domain = expression.OR([domain, [("latin_name", "%", word)]])
                # Categories
                category_mgr = request.env["product.public.category"]
                # Set threshold for pg_trgm for the category search
                request.env.cr.execute(
                    "SELECT set_limit(%f);" % FUZZY_CATEGORY_TRESHOLD
                )
                category_ids = category_mgr.sudo().search(
                    [("name", "%", word)]
                )
                if category_ids:
                    domain = expression.OR(
                        [
                            domain,
                            [("public_categ_ids", "in", category_ids.ids)],
                        ]
                    )
                # Reset threshold for pg_trgm after the category search
                request.env.cr.execute(
                    "SELECT set_limit(%f);" % FUZZY_DEFAULT_TRESHOLD
                )
        # Add sale product domain to domain
        domain = expression.AND([sale_domain, domain])
        return domain

    def _get_search_order(self, post):
        """Order by similarity between search terms and the name of the
        product."""
        order = super()._get_search_order(post)
        if "search" in post:
            order = ("similarity(name, '%s') DESC," % post["search"]) + order
        return order

    @http.route()
    def shop(
        self,
        page=0,
        category=None,
        seedling_months=None,
        search="",
        ppg=False,
        **post
    ):
        # Set product per page
        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG

        # Set threshold for pg_trgm
        request.env.cr.execute(
            "SELECT set_limit(%f);" % FUZZY_DEFAULT_TRESHOLD
        )

        # Preserve compatibility with the website_sale shop function
        # We want all functionnallity that it brings but not the product
        # list.
        response = super().shop(
            page=0,
            category=category,
            seedling_months=seedling_months,
            search=search,
            ppg=0,
            **post
        )

        # Put seedling months in the context so that it is accessible by
        # other function of this controller.
        seedling_month_ids = response.qcontext["seedling_months"]
        if seedling_month_ids:
            context = dict(request.env.context)
            context["seedling_month_ids"] = seedling_month_ids
            request.env.context = context

        # Get all product.template that match the domain
        attrib_values = response.qcontext["attrib_values"]
        products = request.env["product.template"].search(
            self._get_search_domain(search, category, attrib_values),
            order=self._get_search_order(post)
        )

        # Get current user list of products (product.product)
        partner = request.env.user.commercial_partner_id
        if partner.website_restrict_product:
            allowed_products = partner.website_product_ids
        else:
            allowed_products = None

        def variant_ok(product):
            """
            Return True if at least one variant can be sold and at least
            one variant are allowed to be sold to the current user.
            product must be a product.template
            """
            for variant in product.product_variant_ids:
                if (
                    variant.variant_sale_ok
                    and allowed_products is not None
                    and variant in allowed_products
                ):
                    return True
                elif variant.variant_sale_ok and allowed_products is None:
                    return True
            return False

        # Filter products
        products = products.filtered(variant_ok)

        # Construct pager
        keep = response.qcontext["keep"]
        product_count = len(products.ids)
        post.update({key: val for key, val in keep.args.items() if val})
        pager = request.website.pager(
            url=keep.path,
            total=product_count,
            page=page,
            step=ppg,
            scope=7,
            url_args=post
        )

        # Truncate product according to the pager
        products = products[pager["offset"]:pager["offset"]+ppg]

        # Add element to context
        response.qcontext["products"] = products
        response.qcontext["restrict_product"] = (
            partner.website_restrict_product
        )
        response.qcontext["allowed_products"] = allowed_products
        response.qcontext["product_count"] = product_count
        response.qcontext["pager"] = pager
        response.qcontext[
            "get_attribute_value_ids"
        ] = self.get_attribute_value_ids
        return response

    @http.route()
    def product(self, product, category="", search="", **kwargs):
        sm_mgr = request.env["seed.seedling.month"]
        response = super().product(product, category, search, **kwargs)
        response.qcontext["all_seedling_months"] = sm_mgr.sudo().search([])
        return response

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
