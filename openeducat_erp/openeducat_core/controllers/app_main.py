# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<https://www.openeducat.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import hashlib
from odoo import http
from odoo.http import request
import json
import werkzeug.utils
from odoo.addons.portal.controllers.web import Home as OriginalHome


class OpeneducatHome(OriginalHome):

    @http.route()
    def web_login(self, redirect=None, *args, **kw):
        response = super(OpeneducatHome, self).web_login(
            redirect=redirect, *args, **kw)
        if not redirect and request.params.get('login_success'):
            user = request.env['res.users'].browse(request.uid)
            if user.has_group('base.group_user'):
                redirect = '/web?' + request.httprequest.query_string.decode('utf-8')
            else:
                if user.is_parent:
                    redirect = '/my/child'
                else:
                    redirect = '/my'
            return werkzeug.utils.redirect(redirect)
        return response

    def _login_redirect(self, uid, redirect=None):
        if redirect:
            return super(OpeneducatHome, self)._login_redirect(uid, redirect)
        if request.env.user.is_parent:
            return '/my/child'
        return '/my'

    @http.route('/web/loginjson', type='http', auth='public', methods=['POST'], csrf=False)
    def web_login_json(self, redirect=None, *args, **kw):
        # Call the original web_login method
        data = request.jsonrequest  # This captures the JSON payload as a dictionary

        # Access specific variables
        login = data.get('login')
        password = data.get('password')
        passwordenc = hashlib.sha512(password)
        response = super(OpeneducatHome, self).web_login(
            redirect=redirect, *args, **kw)

        if request.params.get('login_success'):
            user = request.env['res.users'].browse(request.uid)
            if user.has_group('base.group_user'):
                redirect = '/web?' + request.httprequest.query_string.decode('utf-8')
            else:
                if user.is_parent:
                    redirect = '/my/child'
                else:
                    redirect = '/my'

            # Execute your SQL query
            cr = request.env.cr
            login = request.params.get('login')
            password = request.params.get('password')

            query = """
                SELECT 
                    res_users.password AS pass,
                    res_users.login AS username,
                    res_groups.name AS role, 
                    op_student.full_name AS student_name,
                    op_faculty.full_name AS faculty_name,
                    res_partner.complete_name AS parent_name, 
                    op_parent_relationship.name AS relationship
                FROM 
                    res_users
                LEFT JOIN 
                    res_groups ON res_users.id = res_groups.write_uid 
                LEFT JOIN 
                    op_student ON res_users.id = op_student.user_id 
                LEFT JOIN 
                    op_faculty ON res_users.partner_id = op_faculty.partner_id 
                LEFT JOIN 
                    op_parent ON op_parent.user_id = res_users.id 
                LEFT JOIN 
                    res_partner ON res_partner.id = op_parent.name 
                LEFT JOIN 
                    op_parent_relationship ON op_parent.relationship_id = op_parent_relationship.id
                WHERE login = %s AND password = %s;
            """
            cr.execute(query, (login, password))
            result = cr.fetchall()

            # Get the columns from the query
            columns = [desc[0] for desc in cr.description]
            data = [dict(zip(columns, row)) for row in result]

            # Return JSON response
            response_data = {
                'status': 'success',
                'redirect_url': redirect,
                'user_id': user.id,
                'user_name': user.name,
                'user_data': data
            }
            return request.make_response(
                json.dumps(response_data),
                headers=[('Content-Type', 'application/json')]
            )

        # If login failed, return an error response
        return request.make_response(
            json.dumps({'status': 'error', 'message': 'Login failed'}),
            headers=[('Content-Type', 'application/json')]
        )