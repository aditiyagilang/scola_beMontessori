from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Faculty(models.Model):
    _inherit = 'op.faculty'

    employee_id = fields.Many2one('hr.employee', string='Employee', ondelete='set null')
    email = fields.Char(required=True)
    employee_tag_ids = fields.Many2many('hr.employee.category', string='Employee Tags')

    @api.model
    def create(self, vals):
        if not vals.get('email'):
            raise ValidationError("Email is required for Faculty.")
        tag_ids = []
        if vals.get('employee_tag_ids'):
            tag_ids = [id_pair[1] for id_pair in vals['employee_tag_ids'] if id_pair[0] == 6]

        faculty = super().create(vals)

        employee_vals = {
            'name': faculty.name,
            'work_email': faculty.email,
            'job_title': 'Faculty',
            'category_ids': [(6, 0, tag_ids)],
        }
        employee = self.env['hr.employee'].create(employee_vals)
        faculty.employee_id = employee.id

        return faculty
