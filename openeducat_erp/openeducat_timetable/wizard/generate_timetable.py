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

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import calendar
import datetime
import pytz
import time


class GenerateSession(models.TransientModel):
    _name = "generate.time.table"
    _description = "Generate Sessions"
    _rec_name = "course_id"

    lesson_schedule_id = fields.Many2one('op.lesson.session', 'Lesson Schedule')
    course_id = fields.Many2one('op.course', 'Course', required=True)
    classroom_id = fields.Many2one('op.classroom', 'Classroom')
    time_table_lines = fields.One2many('gen.time.table.line', 'gen_time_table', 'Time Table Lines')

    # Domain per hari
    time_table_lines_1 = fields.One2many('gen.time.table.line', 'gen_time_table', 'Senin', domain=[('day', '=', '0')])
    time_table_lines_2 = fields.One2many('gen.time.table.line', 'gen_time_table', 'Selasa', domain=[('day', '=', '1')])
    time_table_lines_3 = fields.One2many('gen.time.table.line', 'gen_time_table', 'Rabu', domain=[('day', '=', '2')])
    time_table_lines_4 = fields.One2many('gen.time.table.line', 'gen_time_table', 'Kamis', domain=[('day', '=', '3')])
    time_table_lines_5 = fields.One2many('gen.time.table.line', 'gen_time_table', 'Jumat', domain=[('day', '=', '4')])
    time_table_lines_6 = fields.One2many('gen.time.table.line', 'gen_time_table', 'Sabtu', domain=[('day', '=', '5')])
    time_table_lines_7 = fields.One2many('gen.time.table.line', 'gen_time_table', 'Minggu', domain=[('day', '=', '6')])

    start_date = fields.Date('Start Date', required=True, default=fields.Date.today)
    end_date = fields.Date('End Date', required=True)

    @api.constrains('start_date', 'end_date')
    def check_dates(self):
        for rec in self:
            if rec.start_date > rec.end_date:
                raise ValidationError(_("End Date cannot be before Start Date."))

    def change_tz(self, date):
        local_tz = pytz.timezone(self.env.user.partner_id.tz or 'GMT')
        local_dt = local_tz.localize(date, is_dst=None)
        utc_dt = local_dt.astimezone(pytz.utc)
        return utc_dt.replace(tzinfo=None)

    def act_gen_time_table(self):
        session_obj = self.env['op.session']
        for session in self:
            for n in range((session.end_date - session.start_date).days + 1):
                curr_date = session.start_date + datetime.timedelta(days=n)
                for line in session.time_table_lines:
                    if int(line.day) == curr_date.weekday():
                        start_time_str = '{:02}:{:02}:00'.format(*divmod(int(line.session_start_time * 60), 60))
                        end_time_str = '{:02}:{:02}:00'.format(*divmod(int(line.session_end_time * 60), 60))

                        start_dt = datetime.datetime.strptime(f"{curr_date} {start_time_str}", '%Y-%m-%d %H:%M:%S')
                        end_dt = datetime.datetime.strptime(f"{curr_date} {end_time_str}", '%Y-%m-%d %H:%M:%S')

                        session_obj.create({
                            'faculty_id': line.faculty_id.id,
                            'course_id': session.course_id.id,
                            'classroom_id': session.classroom_id.id,
                            'start_datetime': self.change_tz(start_dt),
                            'end_datetime': self.change_tz(end_dt),
                            'type': calendar.day_name[int(line.day)],
                            'lesson_schedule_id': line.lesson_schedule_id.id,
                        })

        return {'type': 'ir.actions.act_window_close'}


class GenerateSessionLine(models.TransientModel):
    _name = 'gen.time.table.line'
    _description = 'Generate Time Table Lines'
    _rec_name = 'day'

    gen_time_table = fields.Many2one('generate.time.table', 'Time Table', required=True)
    faculty_id = fields.Many2one('op.faculty', 'Faculty', required=True)
    session_start_time = fields.Float("Start Time", required=True)
    session_end_time = fields.Float("End Time", required=True)
    lesson_schedule_id = fields.Many2one('op.lesson.session', 'Lesson Schedule')
    course_id = fields.Many2one('op.course', 'Course')  
    day = fields.Selection([
        ('0', 'Senin'),
        ('1', 'Selasa'),
        ('2', 'Rabu'),
        ('3', 'Kamis'),
        ('4', 'Jumat'),
        ('5', 'Sabtu'),
        ('6', 'Minggu'),
    ], 'Day', required=True)

