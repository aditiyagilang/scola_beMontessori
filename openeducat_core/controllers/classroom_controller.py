from werkzeug import Response
from odoo import http
import json
from ..library.responses import *

class AttendanceController(http.Controller):
    
    @http.route(
        "/api/get_course/", type="http", auth="user", methods=["GET"], csrf=False
    )
    def get_course(self, **kwargs):
        list_course:list = []

        try:
            dt_course = http.request.env['op.course'].search([])
            
            for obj in dt_course:
                list_course.append({
                    'code': obj.code,
                    'name': obj.name
                })
                
            
            return output_ok(list_course)
            
        except Exception as error:
            res_error = {
                'message': error
            }
            
            return output_bad_request(res_error)
    