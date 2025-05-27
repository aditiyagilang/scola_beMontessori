from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

class LessonSession(models.Model):
    _name = 'op.lesson.session'

    name = fields.Char(string="Nama Sesi", required=True)
    start_time = fields.Char(string="Mulai (HH:MM)", required=True)
    end_time = fields.Char(string="Akhir (HH:MM)", required=True)

    @api.constrains('start_time', 'end_time')
    def _check_time_format(self):
        """ Validasi agar waktu dalam format HH:MM dan start_time lebih kecil dari end_time """
        for record in self:
            if not self._is_valid_time(record.start_time) or not self._is_valid_time(record.end_time):
                raise ValidationError("Format waktu harus HH:MM.")

            start_minutes = self._convert_time_to_minutes(record.start_time)
            end_minutes = self._convert_time_to_minutes(record.end_time)

            if start_minutes >= end_minutes:
                raise ValidationError("Waktu 'Mulai' harus lebih kecil dari 'Akhir'.")

    @staticmethod
    def _is_valid_time(time_str):
        """ Memeriksa apakah format string adalah HH:MM """
        try:
            hours, minutes = map(int, time_str.split(":"))
            return 0 <= hours < 24 and 0 <= minutes < 60
        except ValueError:
            return False

    @staticmethod
    def _convert_time_to_minutes(time_str):
        """ Mengonversi waktu HH:MM ke total menit """
        hours, minutes = map(int, time_str.split(":"))
        return hours * 60 + minutes
