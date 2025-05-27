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
import datetime
import uuid
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class OpExam(models.Model):
    _name = "op.exam"
    _inherit = "mail.thread"
    _description = "Exam"

    session_id = fields.Many2one('op.exam.session', 'Exam Session', domain=[('state', 'not in', ['cancel', 'done'])])
    course_id = fields.Many2one('op.course', related='session_id.course_id', store=True, readonly=True)
    batch_id = fields.Many2one('op.batch', 'Batch', required=True)
    subject_id = fields.Many2one('op.subject', 'Subject', required=True)
    exam_code = fields.Char('Exam Code', size=16, required=True)
    attendees_line = fields.One2many('op.exam.attendees', 'exam_id', 'Attendees', readonly=True)
    start_time = fields.Datetime('Start Time', required=True)
    end_time = fields.Datetime('End Time', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('schedule', 'Scheduled'),
        ('held', 'Held'),
        ('result_updated', 'Result Updated'),
        ('cancel', 'Cancelled'),
        ('done', 'Done')
    ], 'State', readonly=True, default='draft', tracking=True)
    note = fields.Text('Note')
    responsible_id = fields.Many2many('op.faculty', string='Responsible')
    name = fields.Char('Exam', size=256, required=True)
    total_marks = fields.Integer('Total Marks', required=True)
    min_marks = fields.Integer('Passing Marks', required=True)
    active = fields.Boolean(default=True)

    survey_id = fields.Many2one('survey.survey', string='Question Bank', help='Select question bank from Survey module')
    exam_status = fields.Selection([
        ('start', 'Start'),
        ('on_going', 'On Going'),
        ('finish', 'Finish')
    ], string="Exam Status", default='start', tracking=True)

    url_link = fields.Char("Survey Link", compute="_compute_url_link", store=True)

    _sql_constraints = [
        ('unique_exam_code', 'unique(exam_code)', 'Code should be unique per exam!')
    ]

    @api.depends('exam_status', 'survey_id')
    def _compute_url_link(self):
        for record in self:
            if record.survey_id and record.exam_status == 'on_going':
                if not record.survey_id.url_link:
                    record.survey_id._generate_url_link()
                exam_uuid = str(uuid.uuid4())  
                record.url_link = f"{record.survey_id.url_link}/{exam_uuid}"
            elif record.exam_status == 'finish':
                record.url_link = False

    def start_exam(self):
       
        self.write({'exam_status': 'on_going'})
        if self.survey_id:
            self.survey_id._generate_url_link()  
            exam_uuid = str(uuid.uuid4())  
            self.write({'url_link': f"{self.survey_id.url_link}/{exam_uuid}"})


    def finish_exam(self):
        """Set exam status to 'finish' and reset survey link."""
        self.write({'exam_status': 'finish'})
        if self.survey_id:
            self.survey_id.url_link = False  
        self.url_link = False


    @api.constrains('total_marks', 'min_marks')
    def _check_marks(self):
        if self.total_marks <= 0.0 or self.min_marks <= 0.0:
            raise ValidationError(_('Enter proper marks!'))
        if self.min_marks > self.total_marks:
            raise ValidationError(_(
                "Passing Marks can't be greater than Total Marks"))
    
    @api.depends('exam_status')
    def _compute_url_link(self):
        """Generate URL when status is 'on_going'."""
        for record in self:
            if record.exam_status == 'on_going' and not record.url_link:
                record.url_link = f"/survey/start/{uuid.uuid4()}"
            elif record.exam_status == 'finish':
                record.url_link = False

    def write(self, vals):
        res = super(OpExam, self).write(vals)
        for exam in self:
            if 'survey_id' in vals:
                self.env['student_user_exam'].search([('exam_id', '=', exam.id)]).write({
                    'survey_id': vals['survey_id']
                })

            if 'exam_status' in vals and exam.survey_id:
                if exam.exam_status == 'start':
                    exam.survey_id.status = 'start'
                    exam.survey_id.url_link = False
                elif exam.exam_status == 'on_going':
                    exam.survey_id.status = 'on_going'
                    exam.survey_id._generate_url_link()
                elif exam.exam_status == 'finish':
                    exam.survey_id.status = 'finish'
                    exam.survey_id.url_link = False  
        return res


    @api.constrains('start_time', 'end_time')
    def _check_date_time(self):
        session_start = datetime.datetime.combine(
            fields.Date.from_string(self.session_id.start_date),
            datetime.time.min)
        session_end = datetime.datetime.combine(
            fields.Date.from_string(self.session_id.end_date),
            datetime.time.max)
        start_time = fields.Datetime.from_string(self.start_time)
        end_time = fields.Datetime.from_string(self.end_time)
        if start_time > end_time:
            raise ValidationError(_('End Time cannot be set before Start Time.'))
        elif start_time < session_start or start_time > session_end or \
                end_time < session_start or end_time > session_end:
            raise ValidationError(
                _('Exam Time should in between Exam Session Dates.'))

    def act_result_updated(self):
        self.state = 'result_updated'

    def act_done(self):
        self.state = 'done'

    def act_draft(self):
        self.state = 'draft'

    def act_cancel(self):
        self.state = 'cancel'
