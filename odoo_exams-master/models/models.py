# -*- coding: utf-8 -*-
from odoo import models, fields, api

import datetime
import logging
import re
import uuid

class Examination(models.Model):
    _inherit = "survey.survey"

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
#

class SurveyScore(models.Model):
    _inherit = "survey.user_input"

    quizz_score = fields.Float(string="Quiz Score")  
    score = fields.Char(string="Score", compute="_compute_score", store=True)

    @api.depends('quizz_score')
    def _compute_score(self):
        for record in self:
            if record.quizz_score is not None: 
                if record.quizz_score < 70:
                    record.score = "fail"
                else:
                    record.score = "pass"
            else:
                record.score = "undefined"  



