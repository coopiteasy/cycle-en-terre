# Copyright 2020 Coop IT Easy SCRLfs <http://coopiteasy.be>
#   Rémy Taymans <remy@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartnerCustomerType(models.Model):
    _inherit = "res.partner.customer.type"

    default_cart_qty = fields.Integer("Default Cart Quantity", default=1)
