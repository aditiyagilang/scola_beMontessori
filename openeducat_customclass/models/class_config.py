from odoo import models, fields, api

class ClassConfig(models.Model):
    _name = 'class.config'
    _description = 'Class Configuration'

    name = fields.Char(string="Configuration Name", required=True)
    academic_year_id = fields.Many2one(
        'op.academic.year',
        string="Academic Year",
        required=True
    )
    total_classes = fields.Integer(string="Total Classes", compute="_compute_total_classes")
    class_info = fields.One2many(
        'op.class.info', 'class_config_id', string="Class Information"
    )

    @api.depends('class_info')
    def _compute_total_classes(self):
        for record in self:
            record.total_classes = len(record.class_info)

class ClassInfo(models.Model):
    _name = 'op.class.info'
    _description = 'Class Information'

    name = fields.Char(string="Class Name", required=True)
    class_config_id = fields.Many2one(
        'class.config',
        string="Class Configuration",
        ondelete="cascade"
    )
    level = fields.Integer(string="Level", required=True)
    total_students = fields.Integer(string="Total Students")