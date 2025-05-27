# -*- coding: utf-8 -*-
# from odoo import http


# class WebsiteLogin(http.Controller):
#     @http.route('/website_login/website_login', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/website_login/website_login/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('website_login.listing', {
#             'root': '/website_login/website_login',
#             'objects': http.request.env['website_login.website_login'].search([]),
#         })

#     @http.route('/website_login/website_login/objects/<model("website_login.website_login"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('website_login.object', {
#             'object': obj
#         })

