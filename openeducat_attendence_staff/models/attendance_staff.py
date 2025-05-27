# -*- coding: utf-8 -*-
import math
import base64
import face_recognition
import numpy as np
import cv2 
from datetime import datetime, timedelta
import logging
from odoo import models, fields, api, exceptions
import pytz 


_logger = logging.getLogger(__name__)  

from datetime import timedelta
from odoo import models, fields, api

from odoo import models, fields, api
from datetime import datetime, timedelta
import math





class OpAttendanceStaff(models.Model):
    _name = 'op.attendance.staff'  
    _description = 'Attendance Staff'

    uid = fields.Many2one('res.users', string="User", required=True)
    present = fields.Selection([
        ('1', 'Present'),
        ('0', 'Absent')
    ], string="Attendance", required=True, default='0')
    datetime = fields.Datetime(string="Attendance Time", required=True, default=fields.Datetime.now)
    session = fields.Selection([
        ('1', 'CheckIn'),
        ('2', 'CheckOut')
    ], string="Session", required=True, default='1')
    verif = fields.Integer(string="Verification", default=0)
    config_id = fields.Many2one('op.attendance.config', string="Location Config", required=True)

    _sql_constraints = [
        ('unique_attendance_per_day', 'unique(uid, datetime)', 
         'Seorang karyawan hanya dapat memiliki satu catatan kehadiran per hari.')
    ]
    
    @api.model
    def delete_attendance_record_by_id(self, record_id):
        """Menghapus catatan kehadiran berdasarkan ID"""
        record = self.search([('id', '=', record_id)])
        if record:
            record.unlink()
            return {'status': True, 'message': 'Berhasil Menghapus data'}
        return {'status': False, 'message': 'Gagal Menghapus data'}

    @api.model
    def check_location(self, *args, **kwargs):
        data = args[0] if args else kwargs.get('data', {})

        uid = data.get('uid')
        latitude = float(data.get('latitude', 0))  
        longitude = float(data.get('longitude', 0))  

        tz = pytz.timezone('Asia/Jakarta')
        datetime_now = datetime.now(tz).replace(tzinfo=None) 

        config = self.env['op.attendance.config'].search([], limit=1)

        if not config:
            return {'status': False, 'message': 'Konfigurasi lokasi tidak ditemukan.', 'attendance_id': None}

        ref_lat = config.latitude
        ref_lon = config.longitude
        max_distance = config.max_distance

        def haversine(lat1, lon1, lat2, lon2):
            R = 6371000  
            phi1, phi2 = map(math.radians, [lat1, lat2])
            delta_phi = math.radians(lat2 - lat1)
            delta_lambda = math.radians(lon2 - lon1)
            a = (math.sin(delta_phi / 2) ** 2 + 
                math.cos(phi1) * math.cos(phi2) * 
                math.sin(delta_lambda / 2) ** 2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            return R * c

        distance = haversine(latitude, longitude, ref_lat, ref_lon)

        if distance > max_distance:
            return {'status': False, 'message': 'Lokasi di luar jangkauan.', 'attendance_id': None}

        today_start = datetime_now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        today_attendance = self.search([
            ('uid', '=', uid),
            ('datetime', '>=', today_start),
            ('datetime', '<', today_end)
        ])

        unverified_sessions = today_attendance.filtered(lambda att: att.verif == 0)
        if unverified_sessions:
            unverified_sessions.unlink()

        today_attendance = self.search([
            ('uid', '=', uid),
            ('datetime', '>=', today_start),
            ('datetime', '<', today_end)
        ])

        if len(today_attendance) >= 2:
            return {'status': False, 'message': 'Anda sudah check-in dan check-out hari ini. Silakan coba lagi besok.', 'attendance_id': None}

        session = '1' if len(today_attendance) == 0 else '2'
        action_text = "Check-in" if session == '1' else "Check-out"

        attendance = self.create({
            'uid': uid,
            'present': '1',
            'datetime': datetime_now, 
            'session': session,
            'verif': 0,
            'config_id': config.id
        })

        return {'status': True, 'message': f'{action_text} berhasil.', 'attendance_id': attendance.id}

    @api.model
    def get_all_attendance_with_leave(self, uid):
        """Mengambil semua data kehadiran dan menggabungkan dengan data cuti"""

        attendances = self.env['op.attendance.staff'].search([
            ('uid', '=', uid)
        ], order="datetime asc")

        if not attendances:
            return {"message": "Tidak ada data kehadiran ditemukan"}

        first_date = attendances[0].datetime.date()
        last_date = attendances[-1].datetime.date()

        leaves = self.env['op.attendance.permission'].search([
            ('uid', '=', uid),
            ('permission_start', '<=', last_date),
            ('permission_end', '>=', first_date)
        ])

        leave_dates = set()
        for leave in leaves:
            leave_range = (leave.permission_end - leave.permission_start).days + 1
            for i in range(leave_range):
                leave_dates.add(leave.permission_start + timedelta(days=i))

        result = []
        current_date = first_date

        while current_date <= last_date:
            date_str = current_date.strftime("%d-%m-%Y")

            if current_date in leave_dates:
                checkin_time = '-'
                checkout_time = '-'
            else:
                checkin_record = attendances.filtered(lambda att: att.session == '1' and att.datetime.date() == current_date)
                checkout_record = attendances.filtered(lambda att: att.session == '2' and att.datetime.date() == current_date)

                checkin_time = checkin_record.datetime.strftime("%H:%M:%S") if checkin_record else '-'
                checkout_time = checkout_record.datetime.strftime("%H:%M:%S") if checkout_record else '-'

            result.append({
                'tanggal': date_str,
                'checkin': checkin_time,
                'checkout': checkout_time
            })

            current_date += timedelta(days=1)

        return result


    @api.model
    def has_checked_in_today(self, uid):
        today_start = fields.Datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        attendance_today = self.search([
            ('uid', '=', uid),
            ('datetime', '>=', today_start),
            ('datetime', '<', today_end)
        ])

        session_status = {"1": False, "2": False}
        for att in attendance_today:
            if att.session == '1':
                session_status["1"] = True
            elif att.session == '2':
                session_status["2"] = True

        return session_status



        
class BinaryStaff(models.Model):
    _name = 'binary.staff'
    _description = 'Data Wajah Staff'

    uid = fields.Many2one('res.users', string="User", required=True, unique=True)
    face_encoding = fields.Text(string="Face Encoding", required=True)

    @api.model
    def verify_face(self, attendance_id, image_base64):
        """ Verifikasi wajah untuk kehadiran staff. """
        attendance = self.env['op.attendance.staff'].browse(attendance_id)
        if not attendance:
            return {'status': False, 'message': 'Data absensi tidak ditemukan.'}

        try:
            face_image = np.frombuffer(base64.b64decode(image_base64), dtype=np.uint8)
            image_np = cv2.imdecode(face_image, cv2.IMREAD_COLOR)
            rgb_face_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        except Exception as e:
            return {'status': False, 'message': f'Format gambar tidak valid: {str(e)}'}

        face_encodings = face_recognition.face_encodings(rgb_face_image)
        if not face_encodings:
            attendance.unlink()  
            return {'status': False, 'message': 'Tidak ada wajah yang terdeteksi. Silahkan Coba Lagi.'}

        face_encoding_base64 = base64.b64encode(face_encodings[0].tobytes()).decode('utf-8')

        user_face = self.search([('uid', '=', attendance.uid.id)], limit=1)

        if not user_face:
            self.create({
                'uid': attendance.uid.id,
                'face_encoding': face_encoding_base64
            })
            attendance.write({'verif': 1})  
            return {'status': True, 'message': 'Data wajah disimpan. Wajah terverifikasi, absen berhasil.'}

        try:
            stored_encoding_bytes = base64.b64decode(user_face.face_encoding)
            stored_encoding = np.frombuffer(stored_encoding_bytes, dtype=np.float64)
        except Exception as e:
            return {'status': False, 'message': f'Data wajah tidak valid: {str(e)}'}

        match = face_recognition.compare_faces([stored_encoding], face_encodings[0])[0]

        if not match:
            attendance.unlink()  
            return {'status': False, 'message': 'Wajah tidak dikenali. Silahkan Coba Lagi.'}

        attendance.write({'verif': 1})

        return {'status': True, 'message': 'Absen berhasil, wajah terverifikasi.'}


