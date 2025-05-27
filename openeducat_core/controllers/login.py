from werkzeug import Response
from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied, AccessError

from ..library.responses import *

import json
import logging
import functools
import werkzeug.wrappers

_logger = logging.getLogger(__name__)

class AccessToken(http.Controller):

    @http.route(
        "/api/authenticate/", type="http", auth="none", methods=["POST"], csrf=False,
        save_session=False, cors="*"
    )
    def get_token(self):
        
        try:
            byte_string = request.httprequest.data
            data = json.loads(byte_string.decode('utf-8'))
            data = data['params']
            username = data['username']
            password = data['password']
            
            user_id = request.session.authenticate(request.db, username, password)

            env = request.env(user=request.env.user.browse(user_id))
            env['res.users.apikeys.description'].check_access_make_key()
            token = env['res.users.apikeys']._generate("", username)
            user = request.env.user

            user_groups =  user.groups_id.mapped('name')

            payloads = {
                'user_id': user_id,
                'username': username,
                'password': password,
                'user_group': user_groups,
                'token': token
            }

            return output_ok(payloads)

        except:
            return output_forbidden({
                'error_message': 'Invalid username/email or password.'
            })


