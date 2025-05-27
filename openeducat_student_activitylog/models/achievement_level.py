from odoo import models, fields

class StudentAchievementLevel(models.Model):
    _name = 'op.achievement.level'
    _description = 'Student Achievement Level'

    name = fields.Char(string='Name', required=True)
    min_point = fields.Integer(string='Minimum Point', required=True)
    max_point = fields.Integer(string='Maximum Point', required=True)
    color = fields.Integer(string='Color', default=0)  

    _sql_constraints = [
        ('point_range_check', 'CHECK(min_point <= max_point)', 'Minimum point must be less than or equal to maximum point.')
    ]
