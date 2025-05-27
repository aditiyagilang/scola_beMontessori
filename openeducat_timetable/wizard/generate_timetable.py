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

import calendar
import datetime
import pytz
import time

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class GenerateSession(models.TransientModel):
    _name = "generate.time.table"
    _description = "Generate Sessions"
    _rec_name = "course_id"

    lesson_schedule_id = fields.Many2one('op.lesson.session', 'Lesson Schedule', required=False, tracking=True)
    course_id = fields.Many2one('op.course', 'Course', required=False)
    #batch_id = fields.Many2one('op.batch', 'Batch', required=True)
    classroom_id = fields.Many2one('op.classroom', 'Classroom')
    time_table_lines = fields.One2many(
        'gen.time.table.line', 'gen_time_table', 'Time Table Lines')
    time_table_lines_1 = fields.One2many(
        'gen.time.table.line', 'gen_time_table', 'Time Table Lines1',
        domain=[('day', '=', '0')])
    time_table_lines_2 = fields.One2many(
        'gen.time.table.line', 'gen_time_table', 'Time Table Lines2',
        domain=[('day', '=', '1')])
    time_table_lines_3 = fields.One2many(
        'gen.time.table.line', 'gen_time_table', 'Time Table Lines3',
        domain=[('day', '=', '2')])
    time_table_lines_4 = fields.One2many(
        'gen.time.table.line', 'gen_time_table', 'Time Table Lines4',
        domain=[('day', '=', '3')])
    time_table_lines_5 = fields.One2many(
        'gen.time.table.line', 'gen_time_table', 'Time Table Lines5',
        domain=[('day', '=', '4')])
    time_table_lines_6 = fields.One2many(
        'gen.time.table.line', 'gen_time_table', 'Time Table Lines6',
        domain=[('day', '=', '5')])
    time_table_lines_7 = fields.One2many(
        'gen.time.table.line', 'gen_time_table', 'Time Table Lines7',
        domain=[('day', '=', '6')])
    start_date = fields.Date(
        'Start Date', required=True, default=time.strftime('%Y-%m-01'))
    end_date = fields.Date('End Date', required=True)

    @api.constrains('start_date', 'end_date')
    def check_dates(self):
        start_date = fields.Date.from_string(self.start_date)
        end_date = fields.Date.from_string(self.end_date)
        if start_date > end_date:
            raise ValidationError(_("End Date cannot be set before Start Date."))

    #@api.onchange('course_id')
    #def onchange_course(self):
        #if self.batch_id and self.course_id:
        #    if self.batch_id.course_id != self.course_id:
        #        self.batch_id = False
        

    def change_tz(self, date):
        local_tz = pytz.timezone(
            self.env.user.partner_id.tz or 'GMT')
        local_dt = local_tz.localize(date, is_dst=None)
        utc_dt = local_dt.astimezone(pytz.utc)
        utc_dt = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
        return datetime.datetime.strptime(
            utc_dt, "%Y-%m-%d %H:%M:%S")

    def act_gen_time_table(self):
        session_obj = self.env['op.session']
        
        for session in self:
            # print(session)  
            start_date = session.start_date
            end_date = session.end_date
            for n in range((end_date - start_date).days + 1):
                curr_date = start_date + datetime.timedelta(n)
                for line in session.time_table_lines:
                    if int(line.day) == curr_date.weekday():
                        # Format waktu untuk start_time dan end_time
                        session_start_time = '{:02}:{:02}:00'.format(*divmod(int(line.session_start_time * 60), 60))
                        session_end_time = '{:02}:{:02}:00'.format(*divmod(int(line.session_end_time * 60), 60))
                        
                        # Gabungkan tanggal dan waktu
                        final_start_date = datetime.datetime.strptime(f"{curr_date} {session_start_time}", '%Y-%m-%d %H:%M:%S')
                        final_end_date = datetime.datetime.strptime(f"{curr_date} {session_end_time}", '%Y-%m-%d %H:%M:%S')
                        
                        # Konversi zona waktu ke UTC
                        curr_start_date = self.change_tz(final_start_date)
                        curr_end_date = self.change_tz(final_end_date)
                        
                        # Buat session dengan data yang valid
                        session_obj.create({
                            'faculty_id': line.faculty_id.id,
                            'subject_id': line.subject_id.id,
                            'course_id': line.batch_id.course_id.id,  # Ambil course_id dari batch_id
                            'batch_id': line.batch_id.id,
                            'classroom_id': session.classroom_id.id,
                            'start_datetime': curr_start_date,
                            'end_datetime': curr_end_date,
                            'type': calendar.day_name[int(line.day)],
                            'lesson_schedule_id': line.lesson_schedule_id.id,  # Tambahkan relasi lesson_schedule
                        })
        return {'type': 'ir.actions.act_window_close'}


class GenerateSessionLine(models.TransientModel):
    _name = 'gen.time.table.line'
    _description = 'Generate Time Table Lines'
    _rec_name = 'day'

    gen_time_table = fields.Many2one(
        'generate.time.table', 'Time Table', required=True)
    faculty_id = fields.Many2one('op.faculty', 'Faculty', required=True)
    subject_id = fields.Many2one('op.subject', 'Subject', required=True)
    timing_id = fields.Many2one('op.timing', 'Timing')
    session_start_time = fields.Float("Start Time")
    session_end_time = fields.Float("End Time")
    #classroom_id = fields.Many2one('op.classroom', 'Classroom')
    batch_id = fields.Many2one('op.batch', 'Batch', required=True)
    lesson_schedule_id = fields.Many2one('op.lesson.session', 'Lesson Schedule', required=False, tracking=True)
    day = fields.Selection([
        ('0', calendar.day_name[0]),
        ('1', calendar.day_name[1]),
        ('2', calendar.day_name[2]),
        ('3', calendar.day_name[3]),
        ('4', calendar.day_name[4]),
        ('5', calendar.day_name[5]),
        ('6', calendar.day_name[6]),
    ], 'Day', required=True)