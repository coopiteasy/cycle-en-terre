# Copyright 2020 Coop IT Easy SCRLfs <http://coopiteasy.be>
#   Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class Website(models.Model):
    _inherit = "website"

    login_invite = fields.Html(string="Login Invite", translate=True,)
    custom_text = fields.Html(string="Custom Text", translate=True,)
