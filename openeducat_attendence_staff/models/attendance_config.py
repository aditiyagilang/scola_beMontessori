from odoo import models, fields, api

class OpAttendanceConfig(models.Model):
    _name = 'op.attendance.config'
    _description = 'Attendance Configuration'

    name = fields.Char(string="Configuration Name", required=True)
    latitude = fields.Float(string="Latitude", required=True)
    longitude = fields.Float(string="Longitude", required=True)
    max_distance = fields.Integer(string="Max Distance (meters)", required=True)

    latitude_str = fields.Char(string="Latitude (String)", compute="_compute_lat_long_str", store=True)
    longitude_str = fields.Char(string="Longitude (String)", compute="_compute_lat_long_str", store=True)

    @api.depends('latitude', 'longitude')
    def _compute_lat_long_str(self):
        """ Mengubah nilai float latitude & longitude menjadi string tanpa trailing zero """
        for record in self:
            lat_str = f"{record.latitude:.16f}".rstrip('0').rstrip('.') 
            lon_str = f"{record.longitude:.16f}".rstrip('0').rstrip('.') 
            record.latitude_str = lat_str
            record.longitude_str = lon_str

