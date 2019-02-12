# Copyright 2018 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.http import request
from odoo.osv import expression
from odoo.addons.website_sale_product_seeds.controllers.main import (
    WebsiteSale as Base
)

# TODO: use a config to let user configure these values
FUZZY_DEFAULT_TRESHOLD = 0.2
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
            if (isinstance(v, tuple) and len(v) == 3
                    and (v[0] == 'name' and v[1] == 'ilike')):
                domain[i] = (v[0], '%', v[2])
        # Normalize domain
        domain = expression.normalize_domain(domain)
        # Add new field in search domain
        if search:
            for word in search.split(" "):
                # Latin name
                domain = expression.OR([domain, [('latin_name', '%', word)]])
                # Categories
                category_mgr = request.env['product.public.category']
                # Set threshold for pg_trgm for the category search
                request.env.cr.execute(
                    "SELECT set_limit(%f);" % FUZZY_CATEGORY_TRESHOLD
                )
                category_ids = category_mgr.sudo().search(
                    [('name', '%', word)]
                )
                if category_ids:
                    domain = expression.OR([
                        domain,
                        [('public_categ_ids', 'in', category_ids.ids)]
                    ])
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
            order = ("similarity(name, '%s') DESC," % post['search']) + order
        return order

    @http.route()
    def shop(self, page=0, category=None, seedling_months=None, search='',
             ppg=False, **post):
        # Set threshold for pg_trgm
        request.env.cr.execute(
            "SELECT set_limit(%f);" % FUZZY_DEFAULT_TRESHOLD
        )

        response = super().shop(page, category, seedling_months, search,
                                ppg, **post)

        def variants_sale_ok(product):
            """Return True if at least one variant can be sold."""
            for variant in product.product_variant_ids:
                if variant.variant_sale_ok:
                    return True
            return False

        products = response.qcontext['products']
        products = products.filtered(variants_sale_ok)

        # Add element to context
        response.qcontext['products'] = products
        response.qcontext['get_attribute_value_ids'] = (
            self.get_attribute_value_ids
        )
        return response
