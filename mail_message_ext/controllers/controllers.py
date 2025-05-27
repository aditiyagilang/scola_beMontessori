# -*- coding: utf-8 -*-
# from odoo import http


# class MailMessageExt(http.Controller):
#     @http.route('/mail_message_ext/mail_message_ext', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mail_message_ext/mail_message_ext/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mail_message_ext.listing', {
#             'root': '/mail_message_ext/mail_message_ext',
#             'objects': http.request.env['mail_message_ext.mail_message_ext'].search([]),
#         })

#     @http.route('/mail_message_ext/mail_message_ext/objects/<model("mail_message_ext.mail_message_ext"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mail_message_ext.object', {
#             'object': obj
#         })

