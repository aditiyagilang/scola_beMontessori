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
import random
from datetime import datetime




class OpExamSession(models.Model):
    _name = "op.exam.session"
    _inherit = ["mail.thread"]
    _description = "Exam Session"

    name = fields.Char('Exam Session', size=256, required=True, tracking=True)
    course_id = fields.Many2one('op.course', 'Course', required=True, tracking=True)
    batch_ids = fields.Many2many('op.batch', string='Batches', required=True, tracking=True)
    exam_code = fields.Char('Exam Session Code', size=16, required=True, tracking=True)
    start_date = fields.Date('Start Date', required=True, tracking=True)
    end_date = fields.Date('End Date', required=True, tracking=True)
    exam_ids = fields.One2many('op.exam', 'session_id', 'Exam(s)')
    exam_type = fields.Many2one('op.exam.type', 'Exam Type', required=True, tracking=True)
    evaluation_type = fields.Selection(
        [('normal', 'Normal'), ('grade', 'Grade')],
        'Evaluation Type', default="normal", required=True, tracking=True)
    venue = fields.Many2one('res.partner', 'Venue', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('schedule', 'Scheduled'),
        ('held', 'Held'),
        ('cancel', 'Cancelled'),
        ('done', 'Done')
    ], 'State', default='draft', tracking=True)
    active = fields.Boolean(default=True)
    survey_ids = fields.Many2many('survey.survey', string='Question Banks', help='Select question banks from Survey module')

    _sql_constraints = [
        ('unique_exam_session_code', 'unique(exam_code)', 'Code should be unique per exam session!')
    ]




    @api.model
    def create(self, vals):
        """Override create method to automatically create exams when a session is created."""
        session = super(OpExamSession, self).create(vals)
        session.create_exams()  # Panggil create_exams() setelah session dibuat
        return session

    def create_exams(self):
        """Function to create exams automatically based on selected surveys and batches."""
        for session in self:
            subject_ids = self.env['op.course'].browse(session.course_id.id).subject_ids.ids

            for batch in session.batch_ids:
                subject_id = subject_ids[0] if subject_ids else False
                exam = self.env['op.exam'].create({
                    'session_id': session.id,
                    'course_id': session.course_id.id,
                    'batch_id': batch.id,
                    'subject_id': subject_id, 
                    'exam_code': f"{session.exam_code}-{batch.id}",
                    'start_time': session.start_date,
                    'end_time': session.end_date,
                    'name': f"{session.name} - {batch.name}",
                    'total_marks': 100,  
                    'min_marks': 40,  
                    'survey_id': False,  
                })

                student_ids = batch.student_ids.ids

                for student_id in student_ids:
                    self.env['student_user_exam'].create({
                        'student_id': student_id, 
                        'batch_id': batch.id,
                        'exam_id': exam.id,
                        'survey_id': False,  
                    })



    @api.constrains('start_date', 'end_date')
    def _check_date_time(self):
        if self.start_date > self.end_date:
            raise ValidationError(
                _('End Date cannot be set before Start Date.'))

    @api.onchange('course_id')
    def onchange_course(self):
        self.batch_ids = [(5, 0, 0)] 


    def act_draft(self):
        self.state = 'draft'

    def act_schedule(self):
        self.state = 'schedule'

    def act_held(self):
        self.state = 'held'

    def act_done(self):
        self.state = 'done'

    def act_cancel(self):
        self.state = 'cancel'


class StudentUserExam(models.Model):
    _name = 'student_user_exam'
    _description = 'Student User Exam'

    student_id = fields.Many2one('op.student', string='Student', required=True, ondelete='cascade')
    batch_id = fields.Many2one('op.batch', string='Batch', required=True, ondelete='cascade')
    exam_id = fields.Many2one('op.exam', string='Exam', ondelete='set null')  
    survey_id = fields.Many2one('survey.survey', string='Survey', ondelete='set null')
    is_fill = fields.Boolean(string='Is Fill', default=False)
    _sql_constraints = [
        ('unique_student_exam_survey', 
         'unique(student_id, exam_id, survey_id)', 
         'Each student can only have one record per exam or survey!')
    ]

    @api.model
    def get_student_exam_status(self, student_id):
        exams = self.env['student_user_exam'].search([('student_id', '=', student_id)])
        result = []
        today = datetime.today()

        for record in exams:
            status = False
            start_date = None
            end_date = None
            exam_name = None

            if record.exam_id:
                start_date = record.exam_id.start_time
                end_date = record.exam_id.end_time
                exam_status = record.exam_id.exam_status  

                if start_date and end_date:
                    if exam_status == 'on_going':
                        status = 'on_going' if start_date <= today <= end_date else 'finished'
                    elif exam_status == 'finish':
                        status = 'finished'
                    else:
                        status = 'not_started'
                
                exam_name = record.exam_id.name

            elif record.survey_id:
                start_date = record.survey_id.start_datetime
                end_date = record.survey_id.end_datetime

                if start_date and end_date:
                    status = 'on_going' if start_date <= today <= end_date else 'finished'
                
                exam_name = record.survey_id.title

            # Tambahkan pengecekan is_fill
            if record.is_fill:
                status = 'finished'

            result.append({
                'student_id': record.student_id.id,
                'exam_id': record.exam_id.id if record.exam_id else None,
                'survey_id': record.survey_id.id if record.survey_id else None,
                'exam_name': exam_name,
                'status': status,  
                'start_date': start_date,
                'end_date': end_date,
                'is_fill': record.is_fill
            })

        return result
