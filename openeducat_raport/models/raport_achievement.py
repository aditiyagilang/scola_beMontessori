from odoo import models, fields, api
from odoo.exceptions import ValidationError


class RaportAchievement(models.Model):
    _name = 'openeducat_raport.achievement'
    _description = 'Capaian Kompetensi'

    name = fields.Char(string='Nama Tipe', required=True)
    description = fields.Text(string='Keterangan')


    # Menambahkan course_id untuk menyambungkan mata pelajaran
    course_id = fields.Many2one(
        comodel_name='op.course',
        string='Mata Pelajaran',
        required=False  # Optional untuk diisi
    )

    tujuan_ids = fields.One2many(
        comodel_name='openeducat_raport.tujuan',
        inverse_name='achievement_id',
        string='Tujuan Pembelajaran'
    )


class RaportTujuan(models.Model):
    _name = 'openeducat_raport.tujuan'
    _description = 'Tujuan Pembelajaran'

    achievement_id = fields.Many2one(
        comodel_name='openeducat_raport.achievement',
        string='Capaian Kompetensi',
        required=True,
        ondelete='cascade'
    )

    classroom_id = fields.Many2one(
        comodel_name='op.classroom',
        string='Kelas',
        required=True
    )

    course_id = fields.Many2one(
        comodel_name='op.course',
        string='Mata Pelajaran',
        required=True
    )

    # Menambahkan field bab_id untuk bab atau subjek, optional
    bab_id = fields.Many2one(
        comodel_name='op.subject',
        string='Bab (Subject)',
        required=False  # Optional
    )

    code = fields.Char(string='Kode Tujuan')
    description = fields.Text(string='Deskripsi Tujuan')

    name = fields.Char(
        string='Nama Tujuan (Otomatis)',
        compute='_compute_name',
        store=True,
        readonly=True
    )

    @api.depends('achievement_id', 'classroom_id')
    def _compute_name(self):
        for rec in self:
            if rec.achievement_id and rec.classroom_id:
                rec.name = f"{rec.achievement_id.name} - {rec.classroom_id.name}"
            else:
                rec.name = ''
