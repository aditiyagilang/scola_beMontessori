from odoo import models, api

class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids', [])

        if active_model == 'account.move' and len(active_ids) == 1:
            move = self.env['account.move'].browse(active_ids[0])

            if move.exists():
                ref_text = move.ref or move.name or ""
                res['communication'] = ref_text
                keywords = ['SLIP', 'Salary', 'Gaji', 'Net Salary']
                if any(word.lower() in ref_text.lower() for word in keywords):
                    res['payment_type'] = 'outbound' 

        return res

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.model
    def create(self, vals):
        if vals.get('ref') and any(k in vals['ref'].lower() for k in ['slip', 'salary', 'gaji']):
            vals['payment_type'] = 'outbound'
        return super().create(vals)
