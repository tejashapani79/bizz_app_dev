from odoo import models,api,_
from odoo.exceptions import ValidationError

class ProductCategory(models.Model):
    _inherit = 'product.category'

    @api.constrains('name')
    def _constrians_name(self):
        """
            Constraint to ensure the uniqueness of the 'name' field.

            This method enforces that no two records in the model can have the same value for the `name` field.
            It is triggered automatically whenever the `name` field is created or updated.

            If another record with the same name (excluding the current one) is found,
            a ValidationError is raised to prevent duplication.

            Raises:
                ValidationError: If a duplicate name is found in another record.
        """
        for rec in self:
            categ_count = self.search_count([('name','=',rec.name),('id','!=',rec.id)])
            if categ_count:
                raise ValidationError(_(f"You can't add same category name : {rec.name}"))