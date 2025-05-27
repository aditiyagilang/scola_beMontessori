# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class mail_message_ext(models.Model):
#     _name = 'mail_message_ext.mail_message_ext'
#     _description = 'mail_message_ext.mail_message_ext'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

