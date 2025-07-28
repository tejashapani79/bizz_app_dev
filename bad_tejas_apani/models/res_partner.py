from odoo import models,api
from odoo.osv import expression

class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        """
            Override the default name_search method to include search by reference (`ref`) field.

            This method extends the domain used for searching records to allow matches
            not only on the default name fields but also on the `ref` field of the partner.

            Args:
                name (str): The search string entered by the user.
                args (list): Optional list of search domain arguments to further restrict the search.
                operator (str): The operator used for matching (default is 'ilike').
                limit (int): Maximum number of records to return (default is 100).

            Returns:
                list: List of tuples (id, display_name) of matching records.
        """
        domain = args or []
        domain = expression.OR([domain, [('ref', '=', name)]])
        return super(ResPartner, self).name_search(name,domain,operator,limit)

    @api.depends('complete_name', 'email', 'vat', 'state_id', 'country_id', 'commercial_company_name','ref')
    @api.depends_context('show_address', 'partner_show_db_id', 'address_inline', 'show_email', 'show_vat', 'lang')
    def _compute_display_name(self):
        """
            Compute the `display_name` of partners, including their reference (`ref`) if available.

            This method overrides the standard `_compute_display_name` to customize how partner names
            are displayed across the system. If the partner has a reference value (`ref`), the name is
            displayed in the format: "Name [REF]". Otherwise, it falls back to the default logic.

            The method also ensures that only the records with `ref` are passed to the superclass method
            to avoid redundant processing.

            Depends On:
                Fields: complete_name, email, vat, state_id, country_id, commercial_company_name, ref
                Context: show_address, partner_show_db_id, address_inline, show_email, show_vat, lang

            Returns:
                None: Updates the `display_name` field in-place.
            """
        ref_partner = self.browse()
        for rec in self:
            if rec.ref:
                rec.display_name = f"{rec.name} [{rec.ref}]"
                ref_partner |= rec
        super(ResPartner, self-ref_partner)._compute_display_name()

    def name_get(self):
        """
            Override the default name_get to include the partner's reference (`ref`) in the display name.

            This method customizes how partner records are displayed in Many2one fields and other
            relational fields across the Odoo UI. If the partner has a `ref` (reference) value,
            it appends the reference in square brackets after the name.

            Example:
                - If name is "John Doe" and ref is "CUST001", display will be: "John Doe [CUST001]"

            Returns:
                list: A list of tuples (id, display_name) for each record.
        """
        result = []
        for partner in self:
            name = partner.name
            if partner.ref:
                name += f' [{partner.ref}]'
            result.append((partner.id, name))
        return result