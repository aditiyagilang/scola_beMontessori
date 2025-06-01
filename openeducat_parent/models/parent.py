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

class OpParent(models.Model):
    _name = "op.parent"
    _description = "Parent"

    name = fields.Many2one('res.partner', 'Name', required=True)
    user_id = fields.Many2one('res.users', string='User', store=True)
    student_ids = fields.Many2many('op.student', string='Student(s)')
    mobile = fields.Char(string='Mobile', related='name.mobile')
    active = fields.Boolean(default=True)
    relationship_id = fields.Many2one('op.parent.relationship', 'Relation with Student', required=True)
    place_of_birth = fields.Char("Tempat Lahir")
    birth_date = fields.Date("Tanggal Lahir")
    phone = fields.Char("No Telepon")
    email = fields.Char("Email")
    address = fields.Text("Alamat")
    gender = fields.Selection([
        ('m', 'Laki-laki'),
        ('f', 'Perempuan')
    ], string="Jenis Kelamin")
    religion = fields.Selection([
        ('islam', 'Islam'),
        ('kristen', 'Kristen'),
        ('katolik', 'Katolik'),
        ('hindu', 'Hindu'),
        ('buddha', 'Buddha'),
        ('khonghucu', 'Khonghucu'),
    ], string="Agama")
    no_kk = fields.Char("Nomor Kartu Keluarga")
    photo = fields.Binary("Foto")
    photo_filename = fields.Char("Nama File Foto")

    _sql_constraints = [(
        'unique_parent',
        'unique(name)',
        'Can not create parent multiple times!'
    )]

    @api.onchange('name')
    def _onchange_name(self):
        self.user_id = self.name.user_id and self.name.user_id.id or False

    @api.model_create_multi
    @api.model
    def create(self, vals_list):
        res = super(OpParent, self).create(vals_list)
        for record in res:
            if record.name and not record.user_id:
                users_res = self.env['res.users']
                internal_user_group = self.env.ref('base.group_user')  # Grup Internal User
                username = record.name.name.lower().replace(" ", "")
                password_plain = record.name.name.lower().replace(" ", "") + "123"
                email = record.name.email or f"{username}@dummy.com"

                # Membuat pengguna baru dan tetapkan grup orang tua dan grup internal user
                new_user = users_res.create({
                    'name': record.name.name,
                    'login': username,
                    'password': password_plain,
                    'partner_id': record.name.id,
                    'groups_id': [(6, 0, [ internal_user_group.id])],  # Menambahkan grup orang tua dan internal user
                    'tz': self._context.get('tz'),
                    'email': email,
                })

                # Mengaitkan pengguna dengan partner
                record.user_id = new_user
                record.name.user_id = new_user

        return res

    def write(self, vals):
        res = super(OpParent, self).write(vals)
        for record in self:
            if record.name and not record.user_id:
                users_res = self.env['res.users']
                internal_user_group = self.env.ref('base.group_user')  # Grup Internal User
                username = record.name.name.lower().replace(" ", "")
                password_plain = record.name.name.lower().replace(" ", "") + "123"
                email = record.name.email or f"{username}@dummy.com"

                # Membuat pengguna baru dan tetapkan grup orang tua dan grup internal user
                new_user = users_res.create({
                    'name': record.name.name,
                    'login': username,
                    'password': password_plain,
                    'partner_id': record.name.id,
                    'groups_id': [(6, 0, [ internal_user_group.id])],  # Menambahkan grup orang tua dan internal user
                    'tz': self._context.get('tz'),
                    'email': email,
                })

                # Mengaitkan pengguna dengan partner
                record.user_id = new_user
                record.name.user_id = new_user

        return res

    def unlink(self):
        for record in self:
            if record.name.user_id:
                record.name.user_id.child_ids = [(6, 0, [])]
            return super(OpParent, self).unlink()

    def create_parent_user(self):
        template = self.env.ref('openeducat_parent.parent_template_user')
        users_res = self.env['res.users']
        for record in self:
            if not record.name.email:                
                raise ValidationError(_('Update parent email id first.'))
            if not record.name.user_id:
                groups_id = template and template.groups_id or False
                internal_user_group = self.env.ref('base.group_user')  # Grup Internal User
                user_ids = [
                    parent.user_id.id for
                    parent in record.student_ids if parent.user_id]
                user_id = users_res.create({
                    'name': record.name.name,
                    'partner_id': record.name.id,
                    'login': record.name.email,
                    'groups_id': [(6, 0, [ internal_user_group.id])],  # Menambahkan grup orang tua dan internal user
                    "tz": self._context.get("tz"),
                    'child_ids': [(6, 0, user_ids)]
                })
                record.user_id = user_id
                record.name.user_id = user_id




class OpStudent(models.Model):
    _inherit = "op.student"

    parent_ids = fields.Many2many('op.parent', string='Orang Tua')

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        return records

    def write(self, vals):
        return super().write(vals)

    def unlink(self):
        return super().unlink()

    def get_parent(self):
        action = self.env.ref('openeducat_parent.act_open_op_parent_view').read()[0]
        action['domain'] = [('student_ids', 'in', self.ids)]
        return action

class OpSubjectRegistration(models.Model):
    _inherit = "op.subject.registration"

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.user.child_ids:
            raise ValidationError(_('Akses Ditolak!\nOrang tua tidak dapat membuat Pendaftaran Mata Pelajaran.'))
        return super().create(vals_list)

    def write(self, vals):
        if self.env.user.child_ids:
            raise ValidationError(_('Akses Ditolak!\nOrang tua tidak dapat mengubah Pendaftaran Mata Pelajaran.'))
        return super().write(vals)