from odoo import api, fields, models


class Picking(models.Model):
    _inherit = "stock.picking"

    origin_id = fields.Many2one(string="Source Document", comodel_name="sale.order", compute="_compute_origin_id")
    team_id = fields.Many2one(related="origin_id.team_id")

    @api.multi
    @api.depends('origin')
    def _compute_origin_id(self):
        self.ensure_one()
        if self.origin:
            self.origin_id = self.env['sale.order'].search([('name', 'like', self.origin)], limit=1)
        else:
            self.origin_id = False
