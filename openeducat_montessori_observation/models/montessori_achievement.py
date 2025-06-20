from odoo import models, fields

class MontessoriAchievement(models.Model):
    _name = 'montessori.achievement'
    _description = 'Montessori Achievement'

    AREA_SELECTION = [
        ('math', 'Mathematics'),
        ('language', 'Language'),
        ('practical_life', 'Practical Life'),
        ('culture', 'Culture Area'),
        ('sensorial', 'Sensorial Area')
    ]

    area = fields.Selection(AREA_SELECTION, string='Montessori Area', required=True)
    title = fields.Char(string='Achievement Title', required=True)
    sub_achievement = fields.Text(string='Sub-achievement Details')  
