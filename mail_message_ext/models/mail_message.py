from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class MailMessage(models.Model):
    _inherit = 'mail.message'

    # Ganti dari One2many menjadi Many2many
    attachment_data = fields.Many2many(
        'ir.attachment',
        string='Attachments',
        compute='_compute_attachment_data',
        store=True
    )

    def _compute_attachment_data(self):
        for record in self:
            # Cari semua attachment yang terkait dengan mail.message
            attachments = self.env['ir.attachment'].search_read(
                [('res_model', '=', 'mail.message'), ('res_id', '=', record.id)],
                fields=['id', 'name', 'mimetype']
            )

            # Debugging log untuk melihat hasil pencarian
            _logger.info(f"Attachments found for Message {record.id}: {attachments}")

            # Tambahkan URL download ke setiap attachment
            for attachment in attachments:
                attachment['url'] = f"/web/content/{attachment['id']}?download=true&filename={attachment['name']}"

            # Jika ada attachment, simpan ID-nya di attachment_data
            if attachments:
                attachment_ids = [att['id'] for att in attachments]
                record.attachment_data = [(6, 0, attachment_ids)]
            else:
                # Kosongkan Many2many jika tidak ada attachment
                record.attachment_data = [(5, 0, 0)]
