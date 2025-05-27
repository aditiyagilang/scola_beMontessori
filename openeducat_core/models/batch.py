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


class OpBatch(models.Model):
    _name = "op.batch"
    _inherit = "mail.thread"
    _description = "OpenEduCat Batch"

    code = fields.Char('Code', size=32, required=True)
    name = fields.Char('Name', size=32, required=True)
    start_date = fields.Date('Start Date', required=True, default=fields.Date.today())
    end_date = fields.Date('End Date', required=True)
    course_id = fields.Many2one('op.course', 'Course', required=False)
    active = fields.Boolean(default=True)
    classroom_id = fields.Many2one('op.classroom', string='Classroom')
    academic_year_id = fields.Many2one('op.academic.year', 'Academic Year', required=True)
    student_ids = fields.Many2many('op.student', string='Student(s)')
    faculty_id = fields.Many2one('op.faculty', string='Faculty')

    _sql_constraints = [
        ('unique_batch_code', 'unique(code)', 'Code should be unique per batch!')
    ]

    @api.constrains('start_date', 'end_date')
    def check_dates(self):
        """Validasi bahwa `start_date` tidak boleh lebih besar dari `end_date`"""
        for record in self:
            if record.start_date > record.end_date:
                raise ValidationError(_("End Date cannot be set before Start Date."))

    @api.onchange('classroom_id')
    def _onchange_classroom_id(self):
        """Saat classroom dipilih, otomatis ambil student dari `op.student`."""
        if self.classroom_id:
            students = self.env['op.student'].search([('classroom_id', '=', self.classroom_id.id)])
            self.student_ids = [(6, 0, students.ids)]  

    def write(self, vals):
        """Handle perubahan student di batch dan update `op.student.course`."""
        result = super(OpBatch, self).write(vals)

        if 'student_ids' in vals:
            student_ids = []
            removed_student_ids = []

            for operation in vals['student_ids']:
                if isinstance(operation, list) and len(operation) > 2:
                    if operation[0] == 6: 
                        student_ids = operation[2]
                    elif operation[0] == 4:  
                        student_ids.append(operation[1])
                    elif operation[0] == 3:  
                        removed_student_ids.append(operation[1])

            for record in self:
                for student_id in student_ids:
                    existing = self.env['op.student.course'].search([
                        ('student_id', '=', student_id),
                        ('batch_id', '=', record.id),
                        ('course_id', '=', record.course_id.id)
                    ], limit=1)

                    if not existing:
                        self.env['op.student.course'].create({
                            'student_id': student_id,
                            'batch_id': record.id,
                            'course_id': record.course_id.id
                        })
                if removed_student_ids:
                    self.env['op.student.course'].search([
                        ('student_id', 'in', removed_student_ids),
                        ('batch_id', '=', record.id),
                        ('course_id', '=', record.course_id.id)
                    ]).unlink()

        return result

    @api.model
    def create(self, vals):
        """Saat batch dibuat, otomatis ambil student dari classroom jika `student_ids` kosong."""
        classroom_id = vals.get('classroom_id')
        student_ids = []

        if not vals.get('student_ids') and classroom_id:
            students = self.env['op.student'].search([('classroom_id', '=', classroom_id)])
            student_ids = students.ids  
        vals.pop('student_ids', None)

        batch = super(OpBatch, self).create(vals)
        if student_ids:
            batch.write({'student_ids': [(6, 0, student_ids)]})
        for student_id in student_ids:
            existing = self.env['op.student.course'].search([
                ('student_id', '=', student_id),
                ('batch_id', '=', batch.id),
                ('course_id', '=', batch.course_id.id)
            ], limit=1)

            if not existing:
                self.env['op.student.course'].create({
                    'student_id': student_id,
                    'batch_id': batch.id,
                    'course_id': batch.course_id.id
                })

        return batch

    @api.model
    def create_batch_with_manual_students(self, vals):
        """
        Fungsi ini memungkinkan membuat batch dengan student yang dipilih secara manual.
        Jika `student_ids` diberikan, gunakan student tersebut.
        """
        if not vals.get('student_ids'):
            raise ValidationError(_("❌ Student harus dipilih secara manual."))

        student_ids = vals.pop('student_ids', [])

        batch = self.create(vals)
        if student_ids:
            batch.write({'student_ids': [(6, 0, student_ids)]})

        return batch.id