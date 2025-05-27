# -*- coding: utf-8 -*-
# from odoo import http


# class OpeneducatStudentActivitylog(http.Controller):
#     @http.route('/openeducat_student_activitylog/openeducat_student_activitylog', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/openeducat_student_activitylog/openeducat_student_activitylog/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('openeducat_student_activitylog.listing', {
#             'root': '/openeducat_student_activitylog/openeducat_student_activitylog',
#             'objects': http.request.env['openeducat_student_activitylog.openeducat_student_activitylog'].search([]),
#         })

#     @http.route('/openeducat_student_activitylog/openeducat_student_activitylog/objects/<model("openeducat_student_activitylog.openeducat_student_activitylog"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('openeducat_student_activitylog.object', {
#             'object': obj
#         })

