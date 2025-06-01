from odoo import models, fields

class LearningMaterial(models.Model):
    _name = 'e.learning.material'
    _description = 'Learning Material'

    elearning_id = fields.Many2one('e.learning', string='E-Learning', required=True, ondelete='cascade')
    title = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('ongoing', 'Ongoing'),
        ('done', 'Done')
    ], string='Status', default='draft')
    created_date = fields.Date(string='Created Date')
    implementation_date = fields.Date(string='Implementation Date')
    file_data = fields.Binary(string='File')
    file_name = fields.Char(string='File Name')
    file_type = fields.Char(string='File Type')  
    student_work_ids = fields.One2many('e.learning.student.work', 'material_id', string='Student Works')

