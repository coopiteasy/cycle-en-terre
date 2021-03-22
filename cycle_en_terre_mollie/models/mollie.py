from odoo import api, models


class AcquirerMollie(models.Model):
    _inherit = "payment.acquirer"

    @api.multi
    def mollie_form_generate_values(self, values):
        mollie_tx_values = super(
            AcquirerMollie, self
        ).mollie_form_generate_values(values)
        so_reference = (
            self.env["sale.order"]
            .sudo()
            .search([("name", "=", mollie_tx_values.get("OrderId"))])
            .reference
        )
        if so_reference:
            mollie_tx_values.update(
                {"Description": so_reference, "OrderReference": so_reference}
            )
        return mollie_tx_values
