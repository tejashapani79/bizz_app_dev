from odoo import models,fields,api

class StockPicking(models.Model):
    _inherit = "stock.picking"

    tag_ids = fields.Many2many(
        comodel_name='crm.tag',
        relation='stock_picking_crm_tag_refl', column1='picking_id', column2='tag_id',
        string="Tags")
    tag_count = fields.Integer(compute="_compute_tag_count",store=True)

    @api.depends('tag_ids')
    def _compute_tag_count(self):
        """
            Compute the number of tags linked to the record.

            This method calculates the count of related tags (`tag_ids`) and stores
            the result in the `tag_count` field. It is triggered automatically whenever
            `tag_ids` changes.

            Returns:
                None: Updates the `tag_count` field for each record.
            """

        for rec in self:
            rec.tag_count = len(rec.tag_ids)

    def _send_confirmation_email(self):
        """
            Extend the delivery confirmation email to notify the responsible salesperson.

            This method overrides the default `_send_confirmation_email` behavior in the
            `stock.picking` model. After calling the original email logic via `super()`,
            it sends a custom email notification to the salesperson (`user_id`) of the
            related Sales Order (`sale_id`), informing them that the delivery order has been confirmed.

            The email includes:
                - Subject with the delivery or origin name
                - Body mentioning the delivery and related sales order
                - Sender as the current Odoo user
                - Recipient as the salesperson's email

            Skips sending if:
                - No related Sales Order or salesperson
                - Salesperson has no email
                - Current user has no email configured

            Returns:
                None
            """
        super(StockPicking, self)._send_confirmation_email()
        for picking in self:
            salesperson = picking.sale_id.user_id
            if not salesperson or not salesperson.email:
                continue
            if not self.env.user.email:
                continue
            subject = f'Delivery Confirmed for Order: {picking.origin or picking.name}'
            body_html = f"""
                        <p>Hello {salesperson.name},</p>
                        <p>The delivery order <strong>{picking.name}</strong> has been <strong>confirmed</strong>.</p>
                        <p>Related Sales Order: {picking.sale_id.name}</p>
                        <p>Thank you,<br/>Odoo System</p>
                    """
            mail_values = {
                'subject': subject,
                'body_html': body_html,
                'email_to': salesperson.email,
                'email_from': self.env.user.email,
            }
            self.env['mail.mail'].create(mail_values).send()