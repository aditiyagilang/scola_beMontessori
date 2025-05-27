{
    'name': 'Hide Odoo Login and Change URL',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Hide default login and change URL, hide Sign In button',
    'description': 'Hide the default Odoo login page, change the login URL, and remove Sign In button from header.',
    'author': 'Your Name',
    'depends': ['website', 'auth_signup'],
    'data': [
        'views/hide_login_template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/website_login/static/src/css/hide_signin.css',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
