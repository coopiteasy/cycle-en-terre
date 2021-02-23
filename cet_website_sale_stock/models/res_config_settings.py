# Copyright 2021+ Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        IrDefault = self.env["ir.default"].sudo()
        # sets the default value for product product fields
        IrDefault.set(
            "product.product",
            "inventory_availability",
            self.inventory_availability,
        )
        IrDefault.set(
            "product.product",
            "available_threshold",
            self.available_threshold
            if self.inventory_availability == "threshold"
            else None,
        )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        IrDefault = self.env["ir.default"].sudo()
        res.update(
            inventory_availability=IrDefault.get(
                "product.product", "inventory_availability"
            )
            or "never",
            available_threshold=IrDefault.get(
                "product.product", "available_threshold"
            )
            or 5.0,
        )
        return res
