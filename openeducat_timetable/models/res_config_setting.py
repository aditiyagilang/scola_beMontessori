from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_faculty_constraint = fields.Boolean(string="Faculty Constraint")
    is_classroom_constraint = fields.Boolean(string="Classroom Constraint")
    is_course_constraint = fields.Boolean(string="Course Constraint")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        config = self.env['ir.config_parameter'].sudo()
        res.update(
            is_faculty_constraint=config.get_param('timetable.is_faculty_constraint', default='1') == '1',
            is_classroom_constraint=config.get_param('timetable.is_classroom_constraint', default='1') == '1',
            is_course_constraint=config.get_param('timetable.is_course_constraint', default='1') == '1',
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        config = self.env['ir.config_parameter'].sudo()
        config.set_param('timetable.is_faculty_constraint', '1' if self.is_faculty_constraint else '0')
        config.set_param('timetable.is_classroom_constraint', '1' if self.is_classroom_constraint else '0')
        config.set_param('timetable.is_course_constraint', '1' if self.is_course_constraint else '0')
