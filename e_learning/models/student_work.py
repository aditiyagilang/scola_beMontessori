from odoo import models, fields

class StudentWork(models.Model):
    _name = 'e.learning.student.work'
    _description = 'Student Work'

    material_id = fields.Many2one('e.learning.material', string='Learning Material', required=True, ondelete='cascade')
    student_id = fields.Many2one('op.student', string='Student', required=True)
    description = fields.Text(string='Description')
    score = fields.Float(string='Score')
    submitted_at = fields.Datetime(string='Submitted At', default=fields.Datetime.now)

    file_data = fields.Binary(string='File')
    file_name = fields.Char(string='File Name')
    file_type = fields.Char(string='File Type')
    report_id = fields.Many2one(
        'student.progress.report',
        string='Progress Report',
        ondelete='set null'
    )
    
