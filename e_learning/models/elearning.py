from odoo import models, fields


class ELearning(models.Model):
    _name = 'e.learning'
    _description = 'E-Learning Module'

    name = fields.Char(string='Name', required=True)
    classroom_id = fields.Many2one('op.classroom', string='Classroom')
    course_id = fields.Many2one('op.course', string='Course')
    faculty_id = fields.Many2one('op.faculty', string='Faculty')

    material_ids = fields.One2many(
        'e.learning.material',
        'elearning_id',
        string='Learning Materials'
    )
