from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class StudentViolationLog(models.Model):
    _name = 'op.violation.log'
    _description = 'Student Violation Log'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Violation Title", required=True, default="/")

    student_id = fields.Many2one('op.student', string="Student", required=True)
    classroom_id = fields.Many2one('op.classroom', string="Classroom", required=False)

    category_id = fields.Many2one('op.violation.category', string="Violation Category", required=True)
    point = fields.Integer(string="Point", required=True)

    sanction = fields.Text(string="Sanction")
    description = fields.Text(string="Description")

    date = fields.Date(string="Date", default=fields.Date.context_today, required=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)

    status = fields.Selection([
        ('need_approve', 'Need Approval'),
        ('not_approved', 'Not Approved'),
        ('ongoing', 'On Going'),
        ('done', 'Done'),
    ], string="Status", default='need_approve', tracking=True)

    evidence = fields.Binary(string="Evidence", attachment=True)
    evidence_filename = fields.Char(string="Filename")


    @api.constrains('point', 'category_id')
    def _check_point_in_category_range(self):
        for record in self:
            if record.point < record.category_id.min_point or record.point > record.category_id.max_point:
                raise ValidationError(_(
                    "Point %s must be between %s and %s for category '%s'"
                ) % (
                    record.point,
                    record.category_id.min_point,
                    record.category_id.max_point,
                    record.category_id.name
                ))

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('op.violation.log') or '/'
        return super().create(vals)


    def write(self, vals):
        for rec in self:
            old_status = rec.status
            result = super(StudentViolationLog, rec).write(vals)

            new_status = vals.get('status')
            if old_status == 'need_approve' and new_status == 'ongoing':
                if rec.student_id.point is not None:
                    rec.student_id.sudo().point -= rec.point 

        return True
