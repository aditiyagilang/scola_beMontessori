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
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import pytz

week_days = [(calendar.day_name[0], _(calendar.day_name[0])),
             (calendar.day_name[1], _(calendar.day_name[1])),
             (calendar.day_name[2], _(calendar.day_name[2])),
             (calendar.day_name[3], _(calendar.day_name[3])),
             (calendar.day_name[4], _(calendar.day_name[4])),
             (calendar.day_name[5], _(calendar.day_name[5])),
             (calendar.day_name[6], _(calendar.day_name[6]))]


class OpSession(models.Model):
    _name = "op.session"
    _inherit = ["mail.thread"]
    _description = "Sessions"

    lesson_schedule_id = fields.Many2one('op.lesson.session', 'Lesson Schedule', tracking=True)
    name = fields.Char(compute='_compute_name', string='Name', store=True)
    timing_id = fields.Many2one('op.timing', 'Timing', tracking=True)
    date = fields.Date('Date', required=True, default=fields.Date.today, tracking=True)
    start_datetime = fields.Datetime('Start Time', required=True, default=fields.Datetime.now)
    end_datetime = fields.Datetime('End Time', required=True)
    course_id = fields.Many2one('op.course', 'Course', required=True)
    faculty_id = fields.Many2one('op.faculty', 'Faculty', required=True)
    classroom_id = fields.Many2one('op.classroom', 'Classroom')
    color = fields.Integer('Color Index')
    type = fields.Char(compute='_compute_day', string='Day', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Canceled')
    ], string='Status', default='draft')
    active = fields.Boolean(default=True)
    days = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday')
    ], 'Days', group_expand='_expand_groups', store=True)
    timing = fields.Char(compute='_compute_timing')

    @api.depends('start_datetime', 'end_datetime')
    def _compute_timing(self):
        tz = pytz.timezone(self.env.user.tz or 'UTC')
        for session in self:
            session.timing = f"{session.start_datetime.astimezone(tz).strftime('%I:%M%p')} - {session.end_datetime.astimezone(tz).strftime('%I:%M%p')}"

    @api.model
    def _expand_groups(self, days, domain, order):
        return ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    @api.depends('start_datetime')
    def _compute_day(self):
        days = {0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday', 4: 'friday', 5: 'saturday', 6: 'sunday'}
        for record in self:
            record.type = days.get(record.start_datetime.weekday()).capitalize()
            record.days = days.get(record.start_datetime.weekday())

    @api.depends('faculty_id', 'course_id', 'start_datetime', 'end_datetime')
    def _compute_name(self):
        tz = pytz.timezone(self.env.user.tz or 'UTC')
        for session in self:
            if session.faculty_id and session.course_id and session.start_datetime and session.end_datetime:
                session.name = f"{session.faculty_id.name}: {session.course_id.name}: {session.start_datetime.astimezone(tz).strftime('%I:%M%p')} - {session.end_datetime.astimezone(tz).strftime('%I:%M%p')}"

    def lecture_draft(self):
        self.state = 'draft'

    def lecture_confirm(self):
        self.state = 'confirm'

    def lecture_done(self):
        self.state = 'done'

    def lecture_cancel(self):
        self.state = 'cancel'

    @api.constrains('start_datetime', 'end_datetime')
    def _check_date_time(self):
        for rec in self:
            if rec.start_datetime > rec.end_datetime:
                raise ValidationError(_('End Time cannot be set before Start Time.'))

    @api.model_create_multi
    def create(self, values):
        return super().create(values)

    def write(self, vals):
        return super().write(vals)

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Sessions'),
            'template': '/openeducat_timetable/static/xls/op_session.xls'
        }]

    @api.constrains('faculty_id', 'start_datetime', 'end_datetime', 'classroom_id', 'course_id')
    def check_timetable_fields(self):
        res_param = self.env['ir.config_parameter'].sudo()
        faculty_constraint = res_param.get_param('timetable.is_faculty_constraint', default='1')
        classroom_constraint = res_param.get_param('timetable.is_classroom_constraint', default='1')
        course_constraint = res_param.get_param('timetable.is_course_constraint', default='1')

        sessions = self.env['op.session'].search([])

        for session in sessions:
            if self.id == session.id:
                continue

            same_day = self.start_datetime.date() == session.start_datetime.date()
            time_overlap = (
                session.start_datetime.time() < self.start_datetime.time() < session.end_datetime.time() or
                session.start_datetime.time() < self.end_datetime.time() < session.end_datetime.time() or
                self.start_datetime.time() <= session.start_datetime.time() < self.end_datetime.time() or
                self.start_datetime.time() < session.end_datetime.time() <= self.end_datetime.time()
            )

            if faculty_constraint and self.faculty_id.id == session.faculty_id.id and same_day and time_overlap:
                raise ValidationError(_('Jadwal bentrok: Dosen yang sama pada waktu yang sama.'))

            if classroom_constraint and self.classroom_id.id == session.classroom_id.id and same_day and time_overlap:
                raise ValidationError(_('Jadwal bentrok: Ruang kelas yang sama pada waktu yang sama.'))

            if course_constraint and self.course_id.id == session.course_id.id and same_day and time_overlap:
                raise ValidationError(_('Jadwal bentrok: Mata pelajaran yang sama pada waktu yang sama.'))
