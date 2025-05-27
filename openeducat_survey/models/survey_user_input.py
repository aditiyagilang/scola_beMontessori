from odoo import models, fields, api

class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    def action_edit_survey(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Edit Survey',
            'res_model': 'survey.user_input',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
        }
