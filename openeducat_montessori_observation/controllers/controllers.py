# -*- coding: utf-8 -*-
# from odoo import http


# class OpeneducatMontessoriObservation(http.Controller):
#     @http.route('/openeducat_montessori_observation/openeducat_montessori_observation', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/openeducat_montessori_observation/openeducat_montessori_observation/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('openeducat_montessori_observation.listing', {
#             'root': '/openeducat_montessori_observation/openeducat_montessori_observation',
#             'objects': http.request.env['openeducat_montessori_observation.openeducat_montessori_observation'].search([]),
#         })

#     @http.route('/openeducat_montessori_observation/openeducat_montessori_observation/objects/<model("openeducat_montessori_observation.openeducat_montessori_observation"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('openeducat_montessori_observation.object', {
#             'object': obj
#         })

