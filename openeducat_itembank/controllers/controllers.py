# -*- coding: utf-8 -*-
# from odoo import http


# class OpeneducatItembank(http.Controller):
#     @http.route('/openeducat_itembank/openeducat_itembank', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/openeducat_itembank/openeducat_itembank/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('openeducat_itembank.listing', {
#             'root': '/openeducat_itembank/openeducat_itembank',
#             'objects': http.request.env['openeducat_itembank.openeducat_itembank'].search([]),
#         })

#     @http.route('/openeducat_itembank/openeducat_itembank/objects/<model("openeducat_itembank.openeducat_itembank"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('openeducat_itembank.object', {
#             'object': obj
#         })

