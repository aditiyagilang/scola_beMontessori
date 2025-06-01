# -*- coding: utf-8 -*-
# from odoo import http


# class ELearning(http.Controller):
#     @http.route('/e_learning/e_learning', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/e_learning/e_learning/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('e_learning.listing', {
#             'root': '/e_learning/e_learning',
#             'objects': http.request.env['e_learning.e_learning'].search([]),
#         })

#     @http.route('/e_learning/e_learning/objects/<model("e_learning.e_learning"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('e_learning.object', {
#             'object': obj
#         })

