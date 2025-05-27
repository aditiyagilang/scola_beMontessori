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
    _parent_name = False

    partner_id = fields.Many2one(
        'res.partner', 'Partner', required=True, ondelete="cascade"
    )
    full_name = fields.Char('Full Name', required=True)
    nid = fields.Char('National Identity Number', size=16)
    nuptk = fields.Char('NUPTK', size=16, required=True)
    nip = fields.Char('NIP')
    npwp = fields.Char('NPWP')
    employment_status = fields.Selection([
        ('pns', 'PNS'),
        ('p3k', 'PPPK'),
        ('honor', 'Guru Honor Sekolah'),
    ])
    religion = fields.Selection([
        ('islam', 'Islam'),
        ('kristen', 'Kristen'),
        ('katolik', 'Katolik'),
        ('hindu', 'Hindu'),
        ('buddha', 'Buddha'),
        ('khonghucu', 'Khonghucu'),
    ])
    married_status = fields.Selection([
        ('kawin', 'Kawin'),
        ('belumkawin', 'Belum Kawin'),
        ('jandaduda', 'Janda / Duda'),
    ])
    grade = fields.Char('Grade')
    birth_date = fields.Date('Birth Date', required=True)
    place_of_birth = fields.Char('Place of Birth')
    blood_group = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('O', 'O'),
        ('AB', 'AB')
    ], string='Blood Group')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], 'Gender', required=True)

    nationality = fields.Many2one('res.country', 'Nationality',   required=False)
    emergency_contact = fields.Many2one('res.partner', 'Emergency Contact')
    id_number = fields.Char('ID Card Number', size=64)
    login = fields.Char('Login', related='partner_id.user_id.login', readonly=True)
    last_login = fields.Datetime(
        'Latest Connection', readonly=True, related='partner_id.user_id.login_date'
    )

    # Menggunakan Many2many untuk Batch (bisa lebih dari 1)
    faculty_batch_ids = fields.Many2many(
        'op.batch',             
        'faculty_batch_rel',    
        'faculty_id',           
        'batch_id',             
        string='Batch(s)',
        tracking=True,
        required=False,
    )

    # Classroom tidak wajib (boleh kosong)
    classroom_id = fields.Many2one('op.classroom', string='Classroom', required=False)

    emp_id = fields.Many2one('hr.employee', 'HR Employee')
    main_department_id = fields.Many2one(
        'op.department', 'Main Department',
        default=lambda self: self.env.user.dept_id.id or False
    )
    allowed_department_ids = fields.Many2many(
        'op.department', string='Allowed Department',
        default=lambda self: self.env.user.department_ids.ids or False
    )
    active = fields.Boolean(default=True)

    full_name_lp = fields.Char('Life Partner Name')
    nip_lp = fields.Char('NIP Life Partner')
    job_lp = fields.Selection([
        ('pns', 'PNS/TNI/POLRI'),
        ('swasta', 'Karyawan Swasta'),
        ('wiraswasta', 'Wiraswasta'),
        ('no_job', 'Tidak Bekerja'),
        ('other', 'Lainnya'),
    ])

    headmaster_license = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak'),
    ])
    supervision_training = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak'),
    ])
    braille_skill = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak'),
    ])
    sign_lang_skill = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak')
    ])

    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(
                    _("Birth Date can't be greater than current date!")
                )

    @api.onchange('full_name')
    def _onchange_name(self):
        self.name = str(self.full_name)

    @api.model
    def create(self, vals):
        # Proses Batch dari Excel
        if 'batch_names' in vals and vals['batch_names'].strip():
            batch_names = vals.pop('batch_names').split(',')
            batch_ids = [self.getOrCreateBatch(name.strip()) for name in batch_names]
            vals['faculty_batch_ids'] = [(6, 0, batch_ids)]
        else:
            vals['faculty_batch_ids'] = [(6, 0, [])]
        
        # Proses Classroom dari Excel
        if 'classroom_name' in vals and vals['classroom_name'].strip():
            classroom_name = vals.pop('classroom_name').strip()
            classroom = self._get_or_create_classroom(classroom_name)
            vals['classroom_id'] = classroom.id if classroom else False
        else:
            vals['classroom_id'] = False

        if 'full_name' in vals and not vals.get('name'):
            vals['name'] = vals['full_name']
        
        record = super(OpFaculty, self).create(vals)
        record._create_or_update_user()
        return record


    def write(self, vals):
        # Proses Batch dari Excel
        if 'batch_names' in vals and vals['batch_names'].strip():
            batch_names = vals.pop('batch_names').split(',')
            batch_ids = [self.getOrCreateBatch(name.strip()) for name in batch_names]
            vals['faculty_batch_ids'] = [(6, 0, batch_ids)]
        else:
            vals['faculty_batch_ids'] = [(6, 0, [])]

        # Proses Classroom dari Excel
        if 'classroom_name' in vals and vals['classroom_name'].strip():
            classroom_name = vals.pop('classroom_name').strip()
            classroom = self._get_or_create_classroom(classroom_name)
            vals['classroom_id'] = classroom.id if classroom else False
        else:
            vals['classroom_id'] = False

        res = super(OpFaculty, self).write(vals)
        self._create_or_update_user()
        return res

    def _create_or_update_user(self):
        users_res = self.env["res.users"]
        user_group = self.env.ref("base.group_portal")
        faculty_group = self.env.ref("openeducat_core.group_op_faculty")  # Ubah sesuai modul kamu

        for record in self:
            if record.nuptk:
                username = record.nuptk
                password_plain = record.nuptk

                if record.partner_id.user_id:
                    # Update User yang sudah ada
                    record.partner_id.user_id.write({
                        "name": record.name,
                        "login": username,
                        "password": password_plain,
                        "groups_id": [(4, faculty_group.id)],  # Tambahkan ke group_op_faculty
                    })
                else:
                    # Buat User baru dengan akses group_op_faculty
                    new_user = users_res.create({
                        "name": record.name,
                        "login": username,
                        "password": password_plain,
                        "partner_id": record.partner_id.id,
                        "groups_id": [(4, faculty_group.id)],
                        "tz": self._context.get("tz"),
                    })
                    record.partner_id.user_id = new_user


    def getClassroomID(self, classroom_name):
        Classroom = self.env['op.classroom']
        # Cari classroom berdasarkan name
        classroom = Classroom.search([('name', '=', classroom_name)], limit=1)
        if classroom:
            return classroom.id
        else:
            # Bersihkan classroom_name untuk dijadikan code
            classroom_code = classroom_name.replace(" ", "_").upper().strip() or "UNKNOWN"
            
            # Buat classroom baru jika tidak ditemukan
            new_classroom = Classroom.create({
                'name': classroom_name,
                'code': classroom_code,  # Menggunakan name sebagai code
                'active': True
            })
            return new_classroom.id

    def get_default_academic_year(self):
        """Mencari academic year yang sesuai dengan tanggal saat ini atau yang terbaru."""
        AcademicYear = self.env['op.academic.year']
        today = fields.Date.today()

        # Cari academic year yang aktif berdasarkan tanggal saat ini
        academic_year = AcademicYear.search([
            ('start_date', '<=', today),
            ('end_date', '>=', today)
        ], limit=1)

        # Jika tidak ada yang aktif, ambil yang terbaru
        if not academic_year:
            academic_year = AcademicYear.search([], order='end_date desc', limit=1)

        return academic_year.id if academic_year else False

    def getOrCreateBatch(self, batch_name):
        Batch = self.env['op.batch']
        # Cari batch berdasarkan name
        batch = Batch.search([('name', '=', batch_name)], limit=1)
        if batch:
            return batch.id
        else:
            # Gunakan get_default_academic_year untuk mencari academic_year yang aktif
            academic_year_id = self.get_default_academic_year()
            academic_year = self.env['op.academic.year'].browse(academic_year_id)

            # Bersihkan batch_name untuk dijadikan code
            batch_code = batch_name.replace(" ", "_").upper().strip() or "UNKNOWN"
            
            # Buat batch baru jika tidak ditemukan
            new_batch = Batch.create({
                'name': batch_name,
                'code': batch_code,  
                'academic_year_id': academic_year_id,  
                'start_date': fields.Date.today(),  
                'end_date': academic_year.end_date if academic_year else fields.Date.today(),
                'active': True
            })
            return new_batch.id




    # Helper untuk Batch
    def _get_batch_ids(self, batch_names):
        Batch = self.env['op.batch']
        batch_ids = []
        for name in batch_names:
            name = name.strip()
            batch = Batch.search([('name', '=', name)], limit=1)
            if batch:
                batch_ids.append(batch.id)
            else:
                new_batch = Batch.create({'name': name})
                batch_ids.append(new_batch.id)
        return batch_ids

    # Helper untuk Classroom
    def _get_or_create_classroom(self, classroom_name):
        if not classroom_name:
            return False
        Classroom = self.env['op.classroom']
        classroom = Classroom.search([('name', '=', classroom_name)], limit=1)
        if not classroom:
            # Bersihkan classroom_name untuk dijadikan code
            classroom_code = classroom_name.replace(" ", "_").upper().strip() or "UNKNOWN"
            classroom = Classroom.create({
                'name': classroom_name,
                'code': classroom_code,  # Gunakan name yang sudah diolah jadi code
                'active': True
            })
        return classroom

