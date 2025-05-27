from odoo import http
from odoo.http import request
import mimetypes
import werkzeug

class AdmissionController(http.Controller):

    @http.route('/api/download_file/<model>/<int:record_id>/<field>', type='http', auth='public')
    def download_file(self, model, record_id, field):
        # Ambil data file dari model Odoo
        record = request.env[model].browse(record_id)
        file_data = getattr(record, field, False)
        
        if not file_data:
            return werkzeug.exceptions.NotFound("File not found.")
        
        # Tentukan nama file dan tipe MIME dinamis berdasarkan file yang ada
        filename = getattr(record, field + '_filename', field)  # Misalnya, field_filename untuk nama file
        mime_type, _ = mimetypes.guess_type(filename)
        
        if not mime_type:
            mime_type = 'application/octet-stream'  # Default MIME type jika tidak dapat ditebak

        # Set header response untuk mengunduh file
        response = request.make_response(file_data, headers=[
            ('Content-Type', mime_type),
            ('Content-Disposition', f'attachment; filename="{filename}"'),
        ])
        return response
