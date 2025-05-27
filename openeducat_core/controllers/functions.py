from werkzeug import Response
from odoo import http
import json

class UserController(http.Controller):

    def get_current_user(self):
        curr_user = request.env.user
        return curr_user