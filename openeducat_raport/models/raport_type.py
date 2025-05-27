from odoo import models, fields, api

class ExamType(models.Model):
    _name = 'openeducat_raport.exam.type'
    _description = 'Jenis Ujian Raport'

    name = fields.Selection(
        selection=[
            ('uh', 'Ulangan Harian'),
            ('kuis', 'Kuis'),
            ('tugas', 'Tugas'),
            ('uts', 'UTS'),
            ('uas', 'UAS'),
            ('lain', 'Lainnya'),
        ],
        string='Jenis Ujian',
        required=True
    )

    display_name = fields.Char(string='Nama', compute='_compute_display_name', store=True)

    @api.depends('name')
    def _compute_display_name(self):
        label_map = dict(self._fields['name'].selection)
        for record in self:
            record.display_name = label_map.get(record.name, '')


class RaportType(models.Model):
    _name = 'openeducat_raport.type'
    _description = 'Tipe Raport'

    name = fields.Char(string='Nama Tipe', required=True)
    description = fields.Text(string='Keterangan')
    
    classroom_id = fields.Many2one(
        comodel_name='op.classroom', 
        string='Kelas',
        required=True
    )

    exam_type_ids = fields.Many2many(
        comodel_name='openeducat_raport.exam.type', 
        string='Jenis Ujian'
    )
