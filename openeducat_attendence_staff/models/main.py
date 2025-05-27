from odoo import http
from odoo.http import request

class OpAttendanceAPI(http.Controller):

    @http.route('/api/attendance/create', type='json', auth='public', methods=['POST'], csrf=False)
    def create_attendance_api(self, uid, present):

        try:
            attendance = request.env['op.attendance.staff'].sudo().create({
                'uid': uid,
                'present': present
            })
            return {
                "success": True,
                "message": "Attendance recorded successfully",
                "attendance_id": attendance.id
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }
