from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StudentAchievement(models.Model):
    _name = 'op.achievement'
    _description = 'Student Achievement'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Achievement Name", required=True)
    student_id = fields.Many2one('op.student', string="Student", required=True)
    level_id = fields.Many2one('op.achievement.level', string="Achievement Level", required=True)
    point = fields.Integer(string="Point", required=True)
    date = fields.Date(string="Date", required=True)
    classroom_id = fields.Many2one('op.classroom', string='Classroom')

    category = fields.Selection([
        ('academic', 'Academic'),
        ('non_academic', 'Non Academic'),
    ], string="Category", required=True)

    ranking = fields.Char(string="Ranking", help="Masukkan ranking seperti 'Juara 1', 'Juara Harapan', dll.")


    evidence = fields.Binary(string="Evidence", attachment=True)
    evidence_filename = fields.Char(string="Evidence Filename")

    status = fields.Selection([
        ('need_approve', 'Need Approval'),
        ('not_approved', 'Not Approved'),
        ('approved', 'Approved'),
    ], string="Status", default='need_approve', tracking=True)

    @api.constrains('point', 'level_id')
    def _check_point_in_level_range(self):
        for record in self:
            if record.point < record.level_id.min_point or record.point > record.level_id.max_point:
                raise ValidationError(_(
                    "Point %s must be between %s and %s for level '%s'."
                ) % (
                    record.point,
                    record.level_id.min_point,
                    record.level_id.max_point,
                    record.level_id.name
                ))

    def write(self, vals):
        for rec in self:
            old_status = rec.status
            result = super(StudentAchievement, rec).write(vals)
            new_status = vals.get('status')
            if old_status == 'need_approve' and new_status == 'approved':
                if rec.student_id.point is not None:
                    rec.student_id.sudo().point += rec.point
            return result
