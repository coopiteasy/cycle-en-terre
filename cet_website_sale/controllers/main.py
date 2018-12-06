# Copyright 2018 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.addons.website_sale_product_seeds.controllers.main import (
    WebsiteSale as Base
)


class WebsiteSale(Base):

    @http.route()
    def shop(self, page=0, category=None, seedling_months=None, search='',
             ppg=False, **post):
        response = super().shop(page, category, seedling_months, search,
                                ppg, **post)
        # Add element to context
        response.qcontext['get_attribute_value_ids'] = (
            self.get_attribute_value_ids
        )
        return response
