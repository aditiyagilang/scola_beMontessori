# from odoo import models, fields, api, exceptions

# class SurveyUserInputLine(models.Model):
#     _inherit = 'survey.user_input.line'

#     answer_score = fields.Float(string="Answer Score", readonly=False)  # Pastikan tidak readonly di sini

#     def write(self, vals):
#         """ Hanya admin (group_survey_manager) yang bisa edit answer_score """
#         if 'answer_score' in vals:
#             if not self.env.user.has_group('survey.group_survey_manager'):
#                 raise exceptions.AccessError("Anda tidak memiliki izin untuk mengedit nilai.")
#         return super(SurveyUserInputLine, self).write(vals)
