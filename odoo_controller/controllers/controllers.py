# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

# class OdooController(http.Controller):
#     @http.route('/odoo_controller/odoo_controller/', auth='public', methods=['GET'])
#     def index(self, **kw):
#         try:
#             students = request.env['']
#             print("students data: ", students)
#             print("students type: ", type(students))
#         except:
#             return "Student not found"

#         return json.dumps(students)
        # output = "<h1>Student Attended</h1>"
        # output = dict()

        # if students:
        #     for student in students:
        #         print("student : ", student)
        #         output += '<li>' + student['first_name'] + '</li>'

        # return output



        # return "Hello, world"

#     @http.route('/odoo_controller/odoo_controller/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_controller.listing', {
#             'root': '/odoo_controller/odoo_controller',
#             'objects': http.request.env['odoo_controller.odoo_controller'].search([]),
#         })

#     @http.route('/odoo_controller/odoo_controller/objects/<model("odoo_controller.odoo_controller"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_controller.object', {
#             'object': obj
#         })