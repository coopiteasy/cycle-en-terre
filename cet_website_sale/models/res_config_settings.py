# Copyright 2020 Coop IT Easy SCRLfs <http://coopiteasy.be>
#   Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    login_invite = fields.Html(
        string="Custom Login Invite",
        related="website_id.login_invite",
    )
    custom_text = fields.Html(
        string="Custom Text",
        related="website_id.custom_text",
    )
