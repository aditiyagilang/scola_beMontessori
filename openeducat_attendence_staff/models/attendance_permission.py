
from datetime import datetime, timedelta
from odoo import models, fields, api, exceptions



class OpAttendancePermission(models.Model):
    _name = 'op.attendance.permission'
    _description = 'Attendance Permission (Cuti)'

    uid = fields.Many2one('res.users', string="User", required=True, default=lambda self: self.env.user)
    types = fields.Selection([
        ('sick', 'Sick Leave'),
        ('vacation', 'Vacation Leave'),
        ('other', 'Other')
    ], string="Type", required=True)

    reason = fields.Text(string="Reason", required=True)
    support = fields.Binary(string="Supporting File", attachment=True)
    support_filename = fields.Char(string="File Name")

    status = fields.Selection([
        ('filed', 'Filed'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string="Status", default='filed', required=True)

    permission_start = fields.Date(string="Start Date", required=True)
    permission_end = fields.Date(string="End Date", required=True)
    filed_date = fields.Datetime(string="Filed Date", related="create_date", store=True, readonly=True)

    @api.constrains('permission_start', 'permission_end')
    def _check_permission_dates(self):
        """ Pastikan permission_end setelah permission_start """
        for record in self:
            if record.permission_end < record.permission_start:
                raise exceptions.ValidationError("End Date must be after Start Date.")

    @api.constrains('support')
    def _check_support_file_size(self):
        """ Pastikan ukuran file tidak lebih dari 1MB """
        max_size = 1 * 1024 * 1024  
        for record in self:
            if record.support and len(record.support) > max_size:
                raise exceptions.ValidationError("The uploaded file must not exceed 1MB.")

    def action_approve(self):
        """ Fungsi untuk menyetujui cuti """
        for record in self:
            record.status = 'approved'

    def action_reject(self):
        """ Fungsi untuk menolak cuti """
        for record in self:
            record.status = 'rejected'

    @api.model
    def get_permissions_by_user(self, user_id):
        """
        Mengambil data izin cuti berdasarkan user_id.
        """
        permissions = self.search([('uid', '=', user_id)])
        result = []

        for perm in permissions:
            result.append({
                "id": perm.id,
                "types": perm.types,
                "reason": perm.reason,
                "permission_start": perm.permission_start,
                "permission_end": perm.permission_end,
                "status": perm.status,
                "filed_date": perm.filed_date
            })
        
        return result

    @api.model
    def update_permission_status(self, permission_id, new_status):
        """
        Memperbarui status izin cuti berdasarkan ID.
        """
        permission = self.browse(permission_id)
        if not permission:
            return {'status': False, 'message': 'Permission not found'}

        if new_status not in ['filed', 'approved', 'rejected']:
            return {'status': False, 'message': 'Invalid status'}

        permission.status = new_status
        return {'status': True, 'message': f'Status updated to {new_status}'}


    @api.model
    def delete_permission(self, permission_id):
        """
        Menghapus izin cuti berdasarkan ID.
        """
        permission = self.browse(permission_id)
        if not permission:
            return {'status': False, 'message': 'Permission not found'}

        permission.unlink()
        return {'status': True, 'message': 'Permission deleted successfully'}

    @api.model
    def get_all_permissions(self):
        """
        Mengambil semua data izin cuti yang ada di sistem.
        """
        permissions = self.search([])
        result = []

        for perm in permissions:
            result.append({
                "id": perm.id,
                "user": perm.uid.name if perm.uid else "Unknown",
                "types": perm.types,
                "reason": perm.reason,
                "permission_start": perm.permission_start,
                "permission_end": perm.permission_end,
                "status": perm.status,
                "filed_date": perm.filed_date
            })
        
        return result