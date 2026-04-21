# Copyright 2018 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import datetime

from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import WebsiteSale as Base


def start_end_months(months):
    """Example, get months = seed.seedling.month(2, 3, 4, 6, 8) this
    returns :
        [
            [seed.seedling.month(2,), seed.seedling.month(4,)],
            [seed.seedling.month(6,)],
            [seed.seedling.month(8,)],
        ]
    """
    ordered_months = months.sorted(key="sequence")
    result = []
    tmp_sequence = []
    previous_month = None
    for month in ordered_months:
        if not tmp_sequence:
            tmp_sequence.append(month)
        elif previous_month.sequence + 1 != month.sequence:
            if previous_month not in tmp_sequence:
                tmp_sequence.append(previous_month)
            result.append(tmp_sequence)
            tmp_sequence = [month]
        previous_month = month
    if tmp_sequence:
        if tmp_sequence[-1].sequence != previous_month.sequence:
            tmp_sequence.append(previous_month)
        result.append(tmp_sequence)
    return result


def seedling_months_to_list(seedling_months=""):
    if seedling_months:
        return [int(x) for x in seedling_months.split("-")]
    else:
        return []


def seedling_months_to_str(seedling_month_ids=None):
    return "-".join([str(r.id) for r in seedling_month_ids])


def seedling_months_add_to_str(seedling_month_ids, new_month):
    if new_month:
        seedling_month_ids |= new_month
    return seedling_months_to_str(seedling_month_ids)


def seedling_months_del_to_str(seedling_month_ids, del_month):
    if del_month:
        seedling_month_ids -= del_month
    return seedling_months_to_str(seedling_month_ids)


class WebsiteSale(Base):
    def _get_search_domain(self, search, category, attrib_values):
        domain = super()._get_search_domain(search, category, attrib_values)
        if "seedling_month_ids" in request.env.context:
            seedling_month_ids = request.env.context["seedling_month_ids"]
            domain.append(("seedling_month_ids", "in", seedling_month_ids.ids))
        return domain

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
        sm_mgr = request.env["seed.seedling.month"]

        if seedling_months == "now":
            # Get current month
            seedling_month_ids = sm_mgr.sudo().search(
                [("sequence", "=", datetime.date.today().month)]
            )
        else:
            # Split list of id for seedling months
            seedling_month_list = seedling_months_to_list(seedling_months)
            # Get existing seedling months
            seedling_month_ids = sm_mgr.sudo().browse(seedling_month_list)
            seedling_month_ids = seedling_month_ids.filtered(
                lambda r: r.exists()
            )

        seedling_months = seedling_months_to_str(seedling_month_ids)

        # Put seedling months in the context so that it is accessible by
        # other function of this controller.
        if seedling_month_ids:
            context = dict(request.env.context)
            context["seedling_month_ids"] = seedling_month_ids
            request.env.context = context

        # The parent does not take seedling_months as an argument. So we
        # give them in the post arg. This is needed for the pager to
        # work correctly.
        if seedling_months:
            post["seedling_months"] = str(seedling_months)

        response = super().shop(page, category, search, ppg, **post)

        # Build the new `keep` function to keep arguments in the URL
        attrib_list = request.httprequest.args.getlist("attrib")
        keep = QueryURL(
            "/shop",
            category=category and int(category),
            search=search,
            attrib=attrib_list,
            seedling_months=seedling_months and str(seedling_months),
            order=post.get("order"),
            is_display_stand=post.get("is_display_stand")  # from website_sale_customer_type
        )

        # Add element to context
        response.qcontext["keep"] = keep
        response.qcontext["seedling_months"] = seedling_month_ids
        response.qcontext["all_seedling_months"] = sm_mgr.sudo().search([])
        response.qcontext["sm_add2str"] = seedling_months_add_to_str
        response.qcontext["sm_del2str"] = seedling_months_del_to_str

        return response

    @http.route()
    def product(self, product, category="", search="", **kwargs):
        response = super().product(product, category, search, **kwargs)
        response.qcontext["start_end_months"] = start_end_months
        return response
