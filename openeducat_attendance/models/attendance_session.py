# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<https://www.openeducat.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import models, fields


from odoo import models, fields

class OpSession(models.Model):
    _inherit = "op.session"

    attendance_sheet = fields.One2many('op.attendance.sheet', 'session_id', string='Session')

    def get_attendance(self):
        sheet = self.env['op.attendance.sheet'].search([('session_id', '=', self.id)], limit=1)

        # Tanpa batch_id, hanya berdasarkan course_id
        register = self.env['op.attendance.register'].search([
            ('course_id', '=', self.course_id.id)
        ])

        if sheet and self.id == sheet.session_id.id and len(sheet) <= 1:
            view_id = self.env.ref('openeducat_attendance.view_op_attendance_sheet_form').id
            return {
                'name': 'Attendance Sheet',
                'type': 'ir.actions.act_window',
                'res_model': 'op.attendance.sheet',
                'view_type': 'form',
                'view_mode': 'form',
                'views': [(view_id, 'form')],
                'res_id': sheet.id,
                'target': 'current',
                'context': {
                    'default_session_id': self.id,
                    'default_register_id': register.ids,
                },
                'domain': [('session_id', '=', self.id)]
            }

        action = self.env.ref('openeducat_attendance.act_open_op_attendance_sheet_view').read()[0]
        action['domain'] = [('session_id', '=', self.id)]
        action['context'] = {
            'default_session_id': self.id,
            'default_register_id': register.ids,
        }
        return action

