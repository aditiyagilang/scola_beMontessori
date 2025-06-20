from odoo import models, fields, api
import json

class StudentInherit(models.Model):
    _inherit = 'op.student'

    montessori_observation_ids = fields.One2many(
        'montessori.observation',
        'student_id',
        string='Montessori Observations'
    )

    observation_summary_json = fields.Text(
        string='Observation Summary (Text)',
        compute='_compute_observation_summary',
        store=False
    )

    @api.depends('montessori_observation_ids')
    def _compute_observation_summary(self):
        for student in self:
            grouped = {}
            for obs in student.montessori_observation_ids:
                ach = obs.achievement_id
                if not ach:
                    continue
                if ach.id not in grouped:
                    grouped[ach.id] = {
                        'achievement_name': ach.title,  
                        'total_true': 0,
                        'total_false': 0
                    }
                if obs.is_repeated:
                    grouped[ach.id]['total_true'] += 1
                else:
                    grouped[ach.id]['total_false'] += 1
            lines = []
            for val in grouped.values():
                lines.append(f"{val['achievement_name']}: ✅ {val['total_true']} | ❌ {val['total_false']}")
            student.observation_summary_json = "\n".join(lines)



class MontessoriObservation(models.Model):
    _name = 'montessori.observation'
    _description = 'Montessori Observation'

    student_id = fields.Many2one('op.student', string='Student', required=True)
    achievement_id = fields.Many2one('montessori.achievement', string='Achievement', required=True)
    is_repeated = fields.Boolean(string='Repeated Observation')
    notes = fields.Text(string='Observation Notes')
    photo = fields.Binary(string='Photo')
    photo_filename = fields.Char(string='Photo Filename')
