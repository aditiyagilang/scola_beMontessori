from odoo import http
from odoo.http import request

class OpeneducatAttendanceStaff(http.Controller):
    @http.route('/attendance_staff', auth='none', type='json', methods=['POST'])
    def get_attendance_records(self, **kw):
        attendance_records = request.env['op.attendance.staff'].search([])
        attendance_data = [{
            'id': record.id,
            'uid': record.uid.name,
            'present': record.present
        } for record in attendance_records]
        return {'status': 'success', 'attendance_records': attendance_data}

    @http.route('/attendance_staff/create', auth='none', type='json', methods=['POST'])
    def create_attendance(self, **kw):
        uid = kw.get('uid')
        present = kw.get('present')

        if not uid or not present:
            return {'status': 'error', 'message': 'UID dan Present diperlukan'}

        attendance = request.env['op.attendance.staff'].create({
            'uid': uid,
            'present': present
        })
        
        return {
            'status': 'success',
            'attendance_id': attendance.id,
            'uid': attendance.uid.name,
            'present': attendance.present
        }

    @http.route('/web/attendance_staff', auth='public', website=True)
    def list_attendance(self, **kw):
        attendance_records = request.env['op.attendance.staff'].search([])
        return request.render('openeducat_attendence_staff.attendance_list_template', {
            'attendance_records': attendance_records
        })

    @http.route('/web/attendance_staff/create', auth='public', website=True)
    def create_attendance_form(self, **kw):
        return request.render('openeducat_attendence_staff.attendance_create_template', {})
