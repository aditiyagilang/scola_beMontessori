from werkzeug import Response
from odoo import http
from odoo.http import request
from ..library.responses import *
import json

class UserController(http.Controller):
    
    @http.route(
        "/api/get_user_info/", type="http", auth="user", methods=["GET"], csrf=False
    )
    def get_user_info(self, **kwargs):
        
        user = request.env.user
        print("user data : ", user)
        user_data = {
            'id': user.id,
            'name': user.name,
            'login': user.login,
            'email': user.email,
            # Add more fields as needed
        }
        
        return output_ok(user_data)
    