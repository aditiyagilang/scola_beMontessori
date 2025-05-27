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

from odoo import models, fields, api


class OpClassroom(models.Model):
    _name = "op.classroom"
    _description = "Classroom"

    name = fields.Char('Name', size=16, required=True)
    code = fields.Char('Code', size=16, required=True)
    batch_ids = fields.One2many('op.batch', 'classroom_id', string='Batches')
    faculty_id = fields.Many2one('op.faculty', string="Faculty")
    capacity = fields.Integer(string='No of Person')
    facilities = fields.One2many('op.facility.line', 'classroom_id',
                                 string='Facility Lines')
    asset_line = fields.One2many('op.asset', 'asset_id',
                                 string='Asset')
    active = fields.Boolean(default=True)
    _sql_constraints = [
        ('unique_classroom_code',
         'unique(code)', 'Code should be unique per classroom!')]
    @api.onchange('batch_ids')
    def _onchange_batch_ids(self):
        """Update students in batch automatically based on classroom."""
        for classroom in self:
            for batch in classroom.batch_ids:
                students = self.env['op.student'].search([('classroom_id', '=', classroom.id)])
                batch.student_ids = [(6, 0, students.ids)]
