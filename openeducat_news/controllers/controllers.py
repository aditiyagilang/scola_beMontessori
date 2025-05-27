# -*- coding: utf-8 -*-
# from odoo import http


# class OpeneducatNews(http.Controller):
#     @http.route('/openeducat_news/openeducat_news', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/openeducat_news/openeducat_news/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('openeducat_news.listing', {
#             'root': '/openeducat_news/openeducat_news',
#             'objects': http.request.env['openeducat_news.openeducat_news'].search([]),
#         })

#     @http.route('/openeducat_news/openeducat_news/objects/<model("openeducat_news.openeducat_news"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('openeducat_news.object', {
#             'object': obj
#         })

