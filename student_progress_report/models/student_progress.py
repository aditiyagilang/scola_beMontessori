from odoo import models, fields

class StudentProgressReportPhoto(models.Model):
    _name = 'student.progress.report.photo'
    _description = 'Student Progress Report Photo'

    report_id = fields.Many2one('student.progress.report', string='Progress Report', required=True, ondelete='cascade')
    photo = fields.Binary(string='Photo', required=True)
    filename = fields.Char(string='Filename')
    description = fields.Char(string='Description')



class StudentProgressReport(models.Model):
    _name = 'student.progress.report'
    _description = 'Student Progress Report'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    date = fields.Date(string='Report Date', default=fields.Date.context_today)

    student_id = fields.Many2one('op.student', string='Student', required=True)
    student_work_ids = fields.One2many(
        'e.learning.student.work',
        'report_id',
        string='Student Works'
    )

    cognitive_notes = fields.Text(string='Cognitive Notes')
    emotional_notes = fields.Text(string='Emotional Notes')
    language_notes = fields.Text(string='Language Notes')
    physical_notes = fields.Text(string='Physical Development Notes')
    social_notes = fields.Text(string='Social Development Notes')

    activity_photo_ids = fields.One2many('student.progress.report.photo', 'report_id', string='Activity Photos')