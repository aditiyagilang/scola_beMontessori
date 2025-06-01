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

class OpFaculty(models.Model):
    _name = "op.faculty"
    _description = "OpenEduCat Faculty"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {"res.partner": "partner_id"}

    partner_id = fields.Many2one('res.partner', 'Partner', required=True, ondelete="cascade")

    full_name = fields.Char('Nama Lengkap', required=True)
    nik = fields.Char('NIK', size=16, required=True)
    gender = fields.Selection([
        ('male', 'Laki-laki'),
        ('female', 'Perempuan')
    ], string='Jenis Kelamin', required=True)
    place_of_birth = fields.Char('Tempat Lahir', required=True)
    birth_date = fields.Date('Tanggal Lahir', required=True)
    religion = fields.Selection([
        ('islam', 'Islam'),
        ('kristen', 'Kristen'),
        ('katolik', 'Katolik'),
        ('hindu', 'Hindu'),
        ('buddha', 'Buddha'),
        ('khonghucu', 'Khonghucu'),
    ], string='Agama', required=True)
    married_status = fields.Selection([
        ('kawin', 'Kawin'),
        ('belumkawin', 'Belum Kawin'),
        ('jandaduda', 'Janda / Duda'),
    ], string='Status Perkawinan', required=True)
    phone = fields.Char('No HP', required=True)
    email = fields.Char('Email', required=True)
    address = fields.Text('Alamat', required=True)
    photo = fields.Binary('Foto')
    photo_filename = fields.Char('Nama File Foto')

    classroom_id = fields.Many2one('op.classroom', string='Classroom')

    login = fields.Char('Login', related='partner_id.user_id.login', readonly=True)
    last_login = fields.Datetime('Terakhir Login', related='partner_id.user_id.login_date', readonly=True)

    active = fields.Boolean(default=True)

    @api.onchange('full_name')
    def _onchange_name(self):
        self.name = self.full_name

    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date and record.birth_date > fields.Date.today():
                raise ValidationError(_("Tanggal lahir tidak boleh di masa depan."))

    @api.model
    def create(self, vals):
        if 'full_name' in vals and not vals.get('name'):
            vals['name'] = vals['full_name']

        # Handle classroom dari nama (jika pakai Excel/form)
        if 'classroom_name' in vals and vals['classroom_name'].strip():
            classroom = self._get_or_create_classroom(vals.pop('classroom_name').strip())
            vals['classroom_id'] = classroom.id if classroom else False

        record = super().create(vals)
        record._create_or_update_user()
        return record

    def write(self, vals):
        if 'full_name' in vals and not vals.get('name'):
            vals['name'] = vals['full_name']

        if 'classroom_name' in vals and vals['classroom_name'].strip():
            classroom = self._get_or_create_classroom(vals.pop('classroom_name').strip())
            vals['classroom_id'] = classroom.id if classroom else False

        res = super().write(vals)
        self._create_or_update_user()
        return res

    def _create_or_update_user(self):
        users_res = self.env['res.users']
        group_internal = self.env.ref('base.group_user')
        group_faculty = self.env.ref('openeducat_core.group_op_faculty')

        for record in self:
            username = record.nik
            password = record.nik
            email = record.email or f"{username}@example.com"

            if record.partner_id.user_id:
                record.partner_id.user_id.write({
                    'name': record.full_name,
                    'login': username,
                    'password': password,
                    'email': email,
                    'groups_id': [(4, group_faculty.id)]
                })
            else:
                user = users_res.create({
                    'name': record.full_name,
                    'login': username,
                    'password': password,
                    'partner_id': record.partner_id.id,
                    'email': email,
                    'groups_id': [(6, 0, [group_internal.id, group_faculty.id])],
                    'tz': self._context.get('tz'),
                })
                record.partner_id.user_id = user

    def _get_or_create_classroom(self, name):
        classroom = self.env['op.classroom'].search([('name', '=', name)], limit=1)
        if classroom:
            return classroom
        return self.env['op.classroom'].create({
            'name': name,
            'code': name.replace(" ", "_").upper(),
            'active': True
        })