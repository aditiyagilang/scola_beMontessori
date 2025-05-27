from odoo import models, fields, api


from odoo import models, fields, api

class Raport(models.Model):
    _name = 'openeducat_raport.raport'
    _description = 'Raport Siswa'

    student_id = fields.Many2one('op.student', string='Siswa', required=True)
    classroom_id = fields.Many2one('op.classroom', string='Classroom', required=False)
    academic_year_id = fields.Many2one('op.academic.year', string='Tahun Ajaran', required=True)
    academic_term_id = fields.Many2one('op.academic.term', string='Semester', required=True)
    detail_ids = fields.One2many('openeducat_raport.raport_detail', 'raport_id', string='Detail Mata Pelajaran')

    total_score = fields.Float(string="Total Nilai", compute="_compute_total_score", store=True)
    is_full = fields.Boolean(string='Akhir Semster?', default=False)

    status = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('fill', 'Sedang Diisi'),
            ('publish', 'Publish'),
        ],
        string='Status',
        default='draft',
        required=True,
    )

    @api.depends('detail_ids.average_score')
    def _compute_total_score(self):
        for rec in self:
            scores = [detail.average_score for detail in rec.detail_ids if detail.average_score]
            rec.total_score = sum(scores) / len(scores) if scores else 0


class RaportDetail(models.Model):
    _name = 'openeducat_raport.raport_detail'
    _description = 'Detail Raport per Mata Pelajaran'

    raport_id = fields.Many2one('openeducat_raport.raport', string='Raport', ondelete='cascade', required=True)
    course_id = fields.Many2one('op.course', string='Mata Pelajaran', required=True)
    faculty_id = fields.Many2one('op.faculty', string='Guru Pengampu')
    note = fields.Text(string='Catatan')

    score_ids = fields.One2many('openeducat_raport.raport_score', 'detail_id', string='Nilai Penilaian')
    average_score = fields.Float(string="Rata-rata", compute="_compute_avg", store=True)

    signature_image = fields.Binary(string="Tanda Tangan Digital")
    signature_filename = fields.Char(string="Nama File Tanda Tangan")

    status = fields.Selection([
        ('draft', 'Draft'),
        ('fill', 'Sedang Diisi'),
        ('publish', 'Publish')
    ], string='Status', default='draft', required=True)

    @api.depends('score_ids.score')
    def _compute_avg(self):
        for rec in self:
            scores = [s.score for s in rec.score_ids if s.score is not None]
            rec.average_score = sum(scores) / len(scores) if scores else 0

    @api.model
    def create(self, vals):
        detail = super().create(vals)

        if detail.raport_id:
            detail.raport_id._compute_total_score()

        return detail



class RaportScore(models.Model):
    _name = 'openeducat_raport.raport_score'
    _description = 'Nilai Per Tipe Penilaian'

    detail_id = fields.Many2one('openeducat_raport.raport_detail', string='Detail Raport', ondelete='cascade', required=True)
    type_id = fields.Many2one('openeducat_raport.type', string='Tipe Penilaian', required=True)
    score = fields.Float(string='Nilai', required=True)

    criteria_id = fields.Many2one('openeducat_raport.criteria', string='Kriteria')
    achievement_id = fields.Many2one('openeducat_raport.achievement', string='Capaian Kompetensi')

    tujuan_id = fields.Many2one(
        'openeducat_raport.tujuan',
        string='Tujuan Pembelajaran',
        required=True
    )