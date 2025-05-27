# from odoo import models
# from odoo.http import request

# class CustomIrHttp(models.AbstractModel):
#     _inherit = 'ir.http'

#     def session_info(self):
#         # Jika dipanggil sebagai instance method (menggunakan 'self')
#         if isinstance(self, models.AbstractModel):
#             # Panggil session_info bawaan dari ir.http
#             session_info = super(CustomIrHttp, self).session_info()

#         else:
#             # Jika dipanggil sebagai classmethod (menggunakan 'cls')
#             session_info = super(CustomIrHttp, type(self)).session_info()

#         # Tambahkan logika untuk menentukan role
#         user = request.env.user
#         partner = user.partner_id

#         role = "User"  # Default role
#         if partner and getattr(partner, 'is_student', False):
#             role = "Student"
#         elif partner and getattr(partner, 'is_parent', False):
#             role = "Parent"
#         elif user.has_group('openeducat_core.group_op_faculty'):
#             role = "Teacher"

#         # Tambahkan role ke dalam respons session_info
#         session_info['role'] = role
#         return session_info

from odoo import models
from odoo.http import request

class CustomIrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        session_info = super(CustomIrHttp, self).session_info()

        # Cek apakah request dan request.env serta user tersedia
        user = getattr(getattr(request, "env", None), "user", None)
        if not user:
            return session_info  # jangan lanjut kalau belum ada user

        # Tentukan role
        role = "User"
        partner = user.partner_id

        if partner and getattr(partner, 'is_student', False):
            role = "Student"
        elif partner and getattr(partner, 'is_parent', False):
            role = "Parent"
        elif partner and getattr(partner, 'is_counseling', False):
            role = "Counseling"
        elif partner and getattr(partner, 'is_director', False):
            role = "Director"
        elif user.has_group('openeducat_core.group_op_faculty'):
            role = "Teacher"

        session_info['role'] = role
        return session_info
