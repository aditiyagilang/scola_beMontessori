from odoo import models, fields, api
from odoo.exceptions import ValidationError


class RaportCriteria(models.Model):
    _name = 'openeducat_raport.criteria'
    _description = 'Kriteria Ujian Raport'

    name = fields.Char(string='Nama Kriteria', required=True)
    description = fields.Text(string='Keterangan')
    
    min_score = fields.Float(string='Batasan Nilai Awal', required=True)
    max_score = fields.Float(string='Batasan Nilai Akhir', required=True)

    raport_prefix = fields.Char(string='Awalan Deskripsi Raport')

    @api.constrains('min_score', 'max_score')
    def _check_score_range(self):
        for record in self:
            if record.min_score > record.max_score:
                raise ValidationError("Batas nilai awal tidak boleh lebih besar dari batas nilai akhir.")
