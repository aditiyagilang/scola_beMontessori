from odoo import models, fields, api
from odoo.exceptions import ValidationError


# class HrPayslip(models.Model):
#     _inherit = 'hr.payslip'

#     def action_payslip_done(self):
#         res = super().action_payslip_done()
#         for slip in self:
#             if slip.struct_id.paid_by == 'manual': 
#                 continue
#             payment_vals = {
#                 'payment_type': 'outbound',
#                 'partner_type': 'supplier',
#                 'partner_id': slip.employee_id.address_home_id.id,
#                 'amount': slip.net_wage,
#                 'payment_date': slip.date_to,
#                 'journal_id': slip.journal_id.id,
#                 'ref': slip.name,  
#             }
#             payment = self.env['account.payment'].create(payment_vals)
#             payment.action_post()
#         return res
