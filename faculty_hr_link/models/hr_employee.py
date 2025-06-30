from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HREmployee(models.Model):
    _inherit = 'hr.employee'

    work_email = fields.Char(required=True)

    @api.constrains('work_email')
    def _check_email(self):
        for rec in self:
            if not rec.work_email:
                raise ValidationError("Email is required for Employee.")
