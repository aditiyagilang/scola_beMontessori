# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class faculty_hr_link(models.Model):
#     _name = 'faculty_hr_link.faculty_hr_link'
#     _description = 'faculty_hr_link.faculty_hr_link'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

