from odoo import models, fields, api

class AdmissionApplication(models.Model):
    _inherit = 'op.admission'

    course_id = fields.Many2one('op.course', string='Course', required=False)
    batch_id = fields.Many2one('op.batch', string='Batch', required=False)
    full_name = fields.Char(string="Full Name", required=True)
    scool_name = fields.Char(string="School Name", required=True, )
    first_name = fields.Char(string="First Name")
    middle_name = fields.Char(string="Middle Name")
    last_name = fields.Char(string="Last Name")
    nisn = fields.Char(string="NISN")
    zona_ids = fields.One2many('op.admission.zona', 'admission_id', string='Data Zonasi')
    prestasi_ids = fields.One2many('op.admission.prestasi', 'admission_id', string='Data Prestasi')
    afirmasi_ids = fields.One2many('op.admission.afirmasi', 'admission_id', string='Data Afirmasi')
    state = fields.Selection(
        selection_add=[('regis', 'Registered')],
    )

    jenis_pendaftaran = fields.Selection([
        ('baru', 'Siswa Baru'),
        ('pindahan', 'Siswa Pindahan')
    ], string='Jenis Pendaftaran')

    jalur_pendaftaran = fields.Selection([
        ('prestasi', 'Prestasi'),
        ('zonasi', 'Zonasi'),
        ('afirmasi', 'Afirmasi')
    ], string='Jalur Pendaftaran')

    parent_name = fields.Char(string="Nama Orang Tua")
    parent_relation = fields.Selection([
        ('ayah', 'Ayah'),
        ('ibu', 'Ibu'),
        ('wali', 'Wali')
    ], string="Hubungan dengan Siswa")
    parent_job = fields.Char(string="Pekerjaan Orang Tua")
    parent_phone = fields.Char(string="No HP Orang Tua")
    parent_address = fields.Text(string="Alamat Orang Tua")
    parent_marital_status = fields.Selection([
        ('menikah', 'Menikah'),
        ('cerai', 'Cerai'),
        ('lainnya', 'Lainnya')
    ], string="Status Pernikahan")

    @api.onchange('full_name')
    def _split_full_name(self):
        for record in self:
            if record.full_name:
                name_parts = record.full_name.strip().split()
                if len(name_parts) == 1:
                    # Kalau cuma 1 kata
                    record.first_name = name_parts[0]
                    record.middle_name = False
                    record.last_name = False
                elif len(name_parts) == 2:
                    # Kalau 2 kata
                    record.first_name = name_parts[0]
                    record.middle_name = False
                    record.last_name = name_parts[1]
                else:
                    # Kalau lebih dari 2 kata
                    record.first_name = name_parts[0]
                    record.middle_name = ' '.join(name_parts[1:-1])
                    record.last_name = name_parts[-1]
            else:
                record.first_name = False
                record.middle_name = False
                record.last_name = False
