from odoo import models, fields, api, _, exceptions
from odoo.exceptions import ValidationError
from odoo.tools import safe_eval

from odoo.exceptions import ValidationError

class Invoicing(models.Model):
    _inherit = "account.move"


class AccountPaymentRegisterExt(models.TransientModel):
    _inherit = 'account.payment.register'

    upload_image_base64   = fields.Binary(string="Bukti Pembayaran (Gambar)")
    upload_image_filename = fields.Char(string="Nama File Gambar")

    def _create_payments(self):
        payments = super()._create_payments()
        # Pindahkan gambar dari wizard ke payment record nyata
        if self.upload_image_base64:
            payments.write({
                'upload_image_base64':   self.upload_image_base64,
                'upload_image_filename': self.upload_image_filename,
            })
        return payments
    
    def _create_payments(self):
        payments = super()._create_payments()
        if self.upload_image_base64:
            payments.write({
                'upload_image_base64': self.upload_image_base64,
                'upload_image_filename': self.upload_image_filename,
            })

        if payments and self.env.context.get('active_model') == 'account.move':
            active_ids = self.env.context.get('active_ids', [])
            if active_ids:
                payments.write({
                    'invoice_id': active_ids[0],
                })
        return payments




class AccountPayment(models.Model):
    _inherit = 'account.payment'

    upload_image_base64   = fields.Binary(string="Bukti Pembayaran (Gambar)")
    upload_image_filename = fields.Char(string="Nama File Gambar")
    invoice_id = fields.Many2one('account.move', string='Related Invoice') 


