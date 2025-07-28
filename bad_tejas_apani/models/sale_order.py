from odoo import models,fields,api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    has_mrp_production = fields.Boolean(
        string="Has MRP Production", compute="_compute_has_mrp_production", store=False
    )

    @api.depends('order_id.procurement_group_id')
    def _compute_has_mrp_production(self):
        for line in self:
            mo_found = False
            moves = self.env['stock.move'].search([
                ('group_id', '=', line.order_id.procurement_group_id.id),
                ('product_id', '=', line.product_id.id),
                ('sale_line_id', '=', line.id),
            ])

            for move in moves:
                # Check if any of its destination moves are raw material input for MO
                for dest in move.move_dest_ids:
                    if dest.raw_material_production_id:
                        mo_found = True
                        break
                if mo_found:
                    break

            line.has_mrp_production = mo_found