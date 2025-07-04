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

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SessionReport(models.TransientModel):
    _name = "time.table.report"
    _description = "Generate Time Table Report"

    state = fields.Selection(
        [('faculty', 'Faculty'), ('student', 'Student')],
        string='Select', required=True, default='faculty')
    course_id = fields.Many2one('op.course', 'Course')
    faculty_id = fields.Many2one('op.faculty', 'Faculty')
    start_date = fields.Date(
        'Start Date', required=True,
        default=(datetime.today() - relativedelta(
            days=datetime.today().weekday())).strftime('%Y-%m-%d'))
    end_date = fields.Date(
        'End Date', required=True,
        default=(datetime.today() + relativedelta(days=6 - datetime.today().weekday())).strftime('%Y-%m-%d'))

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for session in self:
            if session.end_date < session.start_date:
                raise ValidationError(_('End Date cannot be set before Start Date.'))
            elif session.end_date > (session.start_date + timedelta(days=6)):
                raise ValidationError(_("Select date range for a week!"))

    def gen_time_table_report(self):
        template = self.env.ref('openeducat_timetable.report_teacher_timetable_generate')
        data = self.read(['start_date', 'end_date', 'course_id', 'state', 'faculty_id'])[0]

        if data['state'] == 'student':
            time_table_ids = self.env['op.session'].search([
                ('course_id', '=', data['course_id'][0]),
                ('start_datetime', '>=', data['start_date']),
                ('end_datetime', '<=', data['end_date']),
            ], order='start_datetime asc')
            data.update({'time_table_ids': time_table_ids.ids})
            template = self.env.ref('openeducat_timetable.report_student_timetable_generate')
        else:
            teacher_time_table_ids = self.env['op.session'].search([
                ('start_datetime', '>=', data['start_date']),
                ('end_datetime', '<=', data['end_date']),
                ('faculty_id', '=', data['faculty_id'][0]),
            ], order='start_datetime asc')
            data.update({'teacher_time_table_ids': teacher_time_table_ids.ids})

        return template.report_action(self, data=data)
