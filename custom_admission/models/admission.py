from odoo import models, fields

class AdmissionRegister(models.Model):
    _inherit = 'op.admission.register'

    course_id = fields.Many2one('op.course', string='Course', required=False)
    product_id = fields.Many2one('product.product', string="Course Fees", required=False)
