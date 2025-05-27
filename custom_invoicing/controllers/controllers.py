# -*- coding: utf-8 -*-
# from odoo import http


# class CustomInvoicing(http.Controller):
#     @http.route('/custom_invoicing/custom_invoicing', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_invoicing/custom_invoicing/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_invoicing.listing', {
#             'root': '/custom_invoicing/custom_invoicing',
#             'objects': http.request.env['custom_invoicing.custom_invoicing'].search([]),
#         })

#     @http.route('/custom_invoicing/custom_invoicing/objects/<model("custom_invoicing.custom_invoicing"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_invoicing.object', {
#             'object': obj
#         })

