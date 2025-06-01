# -*- coding: utf-8 -*-
# from odoo import http


# class StudentProgressReport(http.Controller):
#     @http.route('/student_progress_report/student_progress_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/student_progress_report/student_progress_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('student_progress_report.listing', {
#             'root': '/student_progress_report/student_progress_report',
#             'objects': http.request.env['student_progress_report.student_progress_report'].search([]),
#         })

#     @http.route('/student_progress_report/student_progress_report/objects/<model("student_progress_report.student_progress_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('student_progress_report.object', {
#             'object': obj
#         })

