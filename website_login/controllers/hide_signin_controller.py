from odoo import http
from odoo.http import request

class HiddenLogin(http.Controller):
    @http.route('/secret-login', type='http', auth='public', website=True)
    def secret_login(self, **kw):
        # Render form login default Odoo, tetapi diakses melalui /secret-login
        return request.render('web.login')
