# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class openeducat_student_activitylog(models.Model):
#     _name = 'openeducat_student_activitylog.openeducat_student_activitylog'
#     _description = 'openeducat_student_activitylog.openeducat_student_activitylog'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

