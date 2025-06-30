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
            if move.exists() and move.ref:
                res['communication'] = move.ref
        return res
