from odoo import models, fields

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    url = fields.Char(string='Download URL', compute='_compute_url')

    def _compute_url(self):
        for record in self:
            record.url = f"/web/content/{record.id}?download=true&filename={record.name}"
