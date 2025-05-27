# -*- coding: utf-8 -*-
# from odoo import http


# class OpeneducatSurvey(http.Controller):
#     @http.route('/openeducat_survey/openeducat_survey', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/openeducat_survey/openeducat_survey/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('openeducat_survey.listing', {
#             'root': '/openeducat_survey/openeducat_survey',
#             'objects': http.request.env['openeducat_survey.openeducat_survey'].search([]),
#         })

#     @http.route('/openeducat_survey/openeducat_survey/objects/<model("openeducat_survey.openeducat_survey"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('openeducat_survey.object', {
#             'object': obj
#         })

