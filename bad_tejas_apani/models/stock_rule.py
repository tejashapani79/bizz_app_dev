from odoo import models,fields,api

class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _make_po_get_domain(self, company_id, values, partner):
        """
                Extends the domain used to search for existing Purchase Orders during procurement.

                This override adds a condition to restrict the domain to Purchase Orders whose
                order lines contain products belonging to the same product category as the
                product in the current orderpoint.

                :param company_id: ID of the company processing the procurement.
                :param values: A dictionary of values related to the procurement rule,
                               expected to contain 'orderpoint_id'.
                :param partner: The vendor (partner) associated with the procurement.
                :return: A domain (list of tuples) to use for finding matching Purchase Orders.
        """
        domain = super(StockRule, self)._make_po_get_domain(company_id, values, partner)
        domain += (('order_line.product_id.categ_id','in',(values['orderpoint_id'].product_id.categ_id.id,)),)
        return domain