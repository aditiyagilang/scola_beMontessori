from odoo import models, fields, api

class AdmissionZona(models.Model):
    _name = 'op.admission.zona'
    _description = 'Admission Zonasi'

    admission_id = fields.Many2one('op.admission', string="Admission")

    scan_kk = fields.Binary("Scan Foto Kartu Keluarga")
    scan_kk_filename = fields.Char("Nama File KK")
    scan_kk_type = fields.Char("Tipe File KK")

    scan_ijazah = fields.Binary("Scan Ijazah/Raport Terakhir")
    scan_ijazah_filename = fields.Char("Nama File Ijazah")
    scan_ijazah_type = fields.Char("Tipe File Ijazah")

    bukti_pembayaran = fields.Binary("Bukti Pembayaran Pendaftaran")
    bukti_pembayaran_filename = fields.Char("Nama File Bukti Pembayaran")
    bukti_pembayaran_type = fields.Char("Tipe File Bukti Pembayaran")

    pas_foto = fields.Binary("Pas Foto")
    pas_foto_filename = fields.Char("Nama File Pas Foto")
    pas_foto_type = fields.Char("Tipe File Pas Foto")

    latitude_user = fields.Float("Latitude User")
    longitude_user = fields.Float("Longitude User")
    jarak = fields.Float("Jarak ke Sekolah (meter)", compute="_compute_distance", store=True)


    @api.model
    def create_zona_web(self, vals):
        record = self.create(vals)
        return record.read()[0]

class AdmissionPrestasi(models.Model):
    _name = 'op.admission.prestasi'
    _description = 'Admission Prestasi'

    admission_id = fields.Many2one('op.admission', string="Admission")

    scan_kk = fields.Binary("Scan Foto Kartu Keluarga")
    scan_kk_filename = fields.Char("Nama File KK")
    scan_kk_type = fields.Char("Tipe File KK")

    upload_raport = fields.Binary("Upload Raport Semester 1–6")
    upload_raport_filename = fields.Char("Nama File Raport")
    upload_raport_type = fields.Char("Tipe File Raport")

    sertifikat_prestasi = fields.Binary("Sertifikat Prestasi")
    sertifikat_prestasi_filename = fields.Char("Nama File Sertifikat")
    sertifikat_prestasi_type = fields.Char("Tipe File Sertifikat")

    bukti_pembayaran = fields.Binary("Bukti Pembayaran Pendaftaran")
    bukti_pembayaran_filename = fields.Char("Nama File Bukti Pembayaran")
    bukti_pembayaran_type = fields.Char("Tipe File Bukti Pembayaran")

    pas_foto = fields.Binary("Pas Foto")
    pas_foto_filename = fields.Char("Nama File Pas Foto")
    pas_foto_type = fields.Char("Tipe File Pas Foto")

    # Nilai Semester 1
    nilai_bhs_indo_smt1 = fields.Float("Bahasa Indonesia Semester 1")
    nilai_matematika_smt1 = fields.Float("Matematika Semester 1")
    nilai_bhs_inggris_smt1 = fields.Float("Bahasa Inggris Semester 1")
    nilai_ipa_smt1 = fields.Float("IPA Semester 1")

    # Nilai Semester 2
    nilai_bhs_indo_smt2 = fields.Float("Bahasa Indonesia Semester 2")
    nilai_matematika_smt2 = fields.Float("Matematika Semester 2")
    nilai_bhs_inggris_smt2 = fields.Float("Bahasa Inggris Semester 2")
    nilai_ipa_smt2 = fields.Float("IPA Semester 2")

    @api.model
    def create_prestasi_web(self, vals):
        record = self.create(vals)
        return record.read()[0]

class AdmissionAfirmasi(models.Model):
    _name = 'op.admission.afirmasi'
    _description = 'Admission Afirmasi'

    admission_id = fields.Many2one('op.admission', string="Admission")

    scan_kk = fields.Binary("Scan Foto Kartu Keluarga")
    scan_kk_filename = fields.Char("Nama File KK")
    scan_kk_type = fields.Char("Tipe File KK")

    scan_ijazah = fields.Binary("Scan Ijazah/Raport Terakhir")
    scan_ijazah_filename = fields.Char("Nama File Ijazah")
    scan_ijazah_type = fields.Char("Tipe File Ijazah")

    bukti_bansos = fields.Binary("Bukti Bantuan Sosial")
    bukti_bansos_filename = fields.Char("Nama File Bansos")
    bukti_bansos_type = fields.Char("Tipe File Bansos")

    bukti_pembayaran = fields.Binary("Bukti Pembayaran Pendaftaran")
    bukti_pembayaran_filename = fields.Char("Nama File Bukti Pembayaran")
    bukti_pembayaran_type = fields.Char("Tipe File Bukti Pembayaran")

    pas_foto = fields.Binary("Pas Foto")
    pas_foto_filename = fields.Char("Nama File Pas Foto")
    pas_foto_type = fields.Char("Tipe File Pas Foto")

    jenis_bantuan = fields.Selection([
        ('kip', 'Kartu Indonesia Pintar (KIP)'),
        ('pkh', 'Program Keluarga Harapan (PKH)'),
        ('bpnt', 'Bantuan Pangan Non Tunai (BPNT)'),
        ('kartu_sembako', 'Kartu Sembako'),
        ('sktm', 'Surat Keterangan Tidak Mampu (SKTM)'),
        ('jamsoda', 'Penerima Jaminan Sosial Daerah (Jamsoda)'),
    ], string="Jenis Bantuan Sosial")

    @api.model
    def create_afirmasi_web(self, vals):
        record = self.create(vals)
        return record.read()[0]
