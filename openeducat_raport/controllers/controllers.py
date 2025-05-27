# -*- coding: utf-8 -*-
# from odoo import http


# class OpeneducatRaport(http.Controller):
#     @http.route('/openeducat_raport/openeducat_raport', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/openeducat_raport/openeducat_raport/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('openeducat_raport.listing', {
#             'root': '/openeducat_raport/openeducat_raport',
#             'objects': http.request.env['openeducat_raport.openeducat_raport'].search([]),
#         })

#     @http.route('/openeducat_raport/openeducat_raport/objects/<model("openeducat_raport.openeducat_raport"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('openeducat_raport.object', {
#             'object': obj
#         })

