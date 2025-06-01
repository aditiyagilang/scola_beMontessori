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


class OpClassroom(models.Model):
    _name = "op.classroom"
    _description = "Classroom"

    name = fields.Char('Name', size=16, required=True)
    code = fields.Char('Code', size=16, required=True)

    course_ids = fields.One2many('op.course', 'classroom_id', string='Courses')
    faculty_id = fields.Many2one('op.faculty', string="Faculty")
    capacity = fields.Integer(string='No of Person')

    facilities = fields.One2many('op.facility.line', 'classroom_id', string='Facility Lines')
    asset_line = fields.One2many('op.asset', 'asset_id', string='Asset')

    min_age = fields.Integer(string='Minimum Age')
    max_age = fields.Integer(string='Maximum Age')

    status = fields.Selection([
        ('active', 'Active'),
        ('not_active', 'Not Active')
    ], string='Status', default='active', required=True)

    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('unique_classroom_code', 'unique(code)', 'Code should be unique per classroom!')
    ]


    @api.constrains('min_age', 'max_age')
    def _check_age_range(self):
        for record in self:
            if record.min_age and record.max_age and record.min_age > record.max_age:
                raise ValidationError(_("Minimum age cannot be greater than maximum age."))
