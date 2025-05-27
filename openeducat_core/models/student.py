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
import hashlib
import base64


class OpStudentCourse(models.Model):
    _name = "op.student.course"
    _description = "Student Course Details"
    _inherit = "mail.thread"
    _rec_name = "student_id"

    student_id = fields.Many2one(
        "op.student", "Student", ondelete="cascade", tracking=True
    )
    course_id = fields.Many2one("op.course", "Course", required=True, tracking=True)
    batch_id = fields.Many2one("op.batch", "Batch", required=True, tracking=True)
    roll_number = fields.Char("Roll Number", tracking=True)
    subject_ids = fields.Many2many("op.subject", string="Subjects")
    academic_years_id = fields.Many2one("op.academic.year", "Academic Year")
    academic_term_id = fields.Many2one("op.academic.term", "Terms")
    state = fields.Selection(
        [("running", "Running"), ("finished", "Finished")],
        string="Status",
        default="running",
    )

    _sql_constraints = [
        (
            "unique_name_roll_number_id",
            "unique(roll_number,course_id,batch_id,student_id)",
            "Roll Number & Student must be unique per Batch!",
        ),
        (
            "unique_name_roll_number_course_id",
            "unique(roll_number,course_id,batch_id)",
            "Roll Number must be unique per Batch!",
        ),
        (
            "unique_name_roll_number_student_id",
            "unique(student_id,course_id,batch_id)",
            "Student must be unique per Batch!",
        ),
    ]

    @api.model
    def get_import_templates(self):
        return [
            {
                "label": _("Import Template for Student Course Details"),
                "template": "/openeducat_core/static/xls/op_student_course.xls",
            }
        ]


class OpStudent(models.Model):
    _name = "op.student"
    _description = "Student"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _inherits = {"res.partner": "partner_id"}

    partner_id = fields.Many2one(
        "res.partner", 
        string="Partner", 
        required=True, 
        ondelete="cascade"
    )
    point = fields.Integer(string="Point", default=100)
    nid = fields.Char("National Identity Number", size=16)
    full_name = fields.Char("Full Name", required=True, translate=False)
    birth_date = fields.Date("Birth Date")
    place_of_birth = fields.Char("Place of Birth")
    blood_group = fields.Selection(
        [("A", "A"), ("B", "B"), ("O", "O"), ("AB", "AB")], 
        string="Blood Group"
    )
    gender = fields.Selection(
        [("m", "Male"), ("f", "Female"), ("o", "Other")],
        "Gender",
        required=True,
        default="m",
    )
    classroom_id = fields.Many2one('op.classroom', string="Classroom")
    nationality = fields.Many2one("res.country", "Nationality")
    emergency_contact = fields.Many2one("res.partner", "Emergency Contact")
    id_number = fields.Char("ID Card Number", size=64)
    religion = fields.Selection([
        ('islam', 'Islam'),
        ('kristen', 'Kristen'),
        ('katolik', 'Katolik'),
        ('hindu', 'Hindu'),
        ('buddha', 'Buddha'),
        ('khonghucu', 'Khonghucu'),
    ])
    user_id = fields.Many2one("res.users", "User", ondelete="cascade")
    category_id = fields.Many2one("op.category", "Category")
    course_detail_ids = fields.One2many(
        "op.student.course", "student_id", "Course Details", tracking=True
    )
    active = fields.Boolean(default=True)
    sic = fields.Char("Student Identification Number", size=20)
    nsn = fields.Char("National Student Number", size=10, required=True)

    _sql_constraints = [
        (
            "unique_sic",
            "unique(sic)",
            "Student Identification Number must be unique per student!",
        ),
        (
            "unique_nsn",
            "unique(nsn)",
            "National Student Number must be unique per student!",
        )
    ]

    @api.onchange("full_name")
    def _onchange_name(self):
        if self.full_name:
            self.name = str(self.full_name)

    @api.constrains("birth_date")
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(
                    _("Birth Date can't be greater than current date!")
                )

    @api.model
    def get_import_templates(self):
        return [
            {
                "label": _("Import Template for Students"),
                "template": "/openeducat_core/static/xls/op_student.xls",
            }
        ]

    @api.model
    def create(self, vals):
        if 'point' not in vals:
            vals['point'] = 100
        record = super(OpStudent, self).create(vals)
        record._create_or_update_user()
        return record


    def write(self, vals):
        res = super(OpStudent, self).write(vals)
        self._create_or_update_user()
        return res

    def _create_or_update_user(self):
        users_res = self.env["res.users"]
        user_group = self.env.ref("base.group_user")  # Ganti dengan group_internal_user, bukan portal

        for record in self:
            if record.nsn:
                username = record.nsn
                password_plain = record.nsn
                password_encrypted = password_plain
                if record.user_id:
                    record.user_id.write({
                        "name": record.name,
                        "login": username,
                        "password": password_encrypted,
                    })
                else:
                    user_id = users_res.create({
                        "name": record.name,
                        "login": username,
                        "password": password_encrypted,
                        "partner_id": record.partner_id.id,
                        "groups_id": [(6, 0, [user_group.id])],  # Menggunakan group_user untuk Internal User
                        "is_student": True,
                        "tz": self._context.get("tz"),
                    })
                    record.user_id = user_id

    def create_student_user(self):
        for record in self:
            if not record.nsn:
                raise ValidationError(_("NSN harus diisi untuk membuat user."))
            if record.user_id:
                raise ValidationError(_("User sudah dibuat untuk student ini."))

            username = record.nsn
            password_plain = record.nsn
            password_encrypted = password_plain

            # Membuat user dengan Internal User group
            user_id = self.env["res.users"].create({
                "name": record.name,
                "login": username,
                "password": password_encrypted,
                "partner_id": record.partner_id.id,
                "groups_id": [(6, 0, [self.env.ref("base.group_user").id])],  # Internal User group
                "is_student": True,
                "tz": self._context.get("tz"),
            })
            record.user_id = user_id
