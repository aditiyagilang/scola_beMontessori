from odoo import models, fields

class ViolationCategory(models.Model):
    _name = 'op.violation.category'
    _description = 'Violation Category'

    name = fields.Char(string='Category Name', required=True)
    min_point = fields.Integer(string='Minimum Point', required=True)
    max_point = fields.Integer(string='Maximum Point', required=True)
    color = fields.Selection(
        [(str(i), f'Color {i}') for i in range(1, 6)],
        string='Color', default='1', required=True
    )


