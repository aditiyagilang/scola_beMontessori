from odoo import models, fields, api, exceptions

class MailChannel(models.Model):
    _inherit = 'discuss.channel'

    is_readonly = fields.Boolean(string="Readonly Channel", default=False)

    @api.model
    def message_post(self, **kwargs):
        if self.is_readonly and self.env.user.id not in self.channel_partner_ids.mapped('id'):
            raise exceptions.AccessError("You cannot post messages in this readonly channel.")
        return super(MailChannel, self).message_post(**kwargs)