# -*- coding: utf-8 -*-
# from odoo import http


# class FacultyHrLink(http.Controller):
#     @http.route('/faculty_hr_link/faculty_hr_link', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/faculty_hr_link/faculty_hr_link/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('faculty_hr_link.listing', {
#             'root': '/faculty_hr_link/faculty_hr_link',
#             'objects': http.request.env['faculty_hr_link.faculty_hr_link'].search([]),
#         })

#     @http.route('/faculty_hr_link/faculty_hr_link/objects/<model("faculty_hr_link.faculty_hr_link"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('faculty_hr_link.object', {
#             'object': obj
#         })

