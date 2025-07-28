from odoo import models

class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_new_picking_values(self):
        """
            Extend the picking values with sales order tags when creating a new stock picking.

            This method overrides the base `_get_new_picking_values` to include the `tag_ids`
            from the related Sales Order (`sale_line_id.order_id`). This ensures that any tags
            assigned to the Sales Order are also passed to the generated picking.

            Returns:
                dict: A dictionary of values to be used when creating a new stock picking,
                      including any additional fields such as `tag_ids` if applicable.
            """
        vals = super(StockMove, self)._get_new_picking_values()
        if self.sale_line_id:
            vals.update({'tag_ids' : self.sale_line_id.order_id.tag_ids})
        return vals