# -*- coding: utf-8 -*-
{
    'name': "Examination",
    'summary': "Module untuk ujian berbasis Odoo menggunakan Survey.",
    'description': """
        Modul ini memungkinkan pengguna untuk membuat dan mengelola ujian menggunakan fitur yang ada di modul survey Odoo.
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Education',
    'version': '17.0.1.0.0',
    'license': 'LGPL-3',

    # Dependensi modul
    'depends': ['base', 'survey'],

    # Data yang akan dimuat
    'data': [
        'security/ir.model.access.csv',  # Aktifkan jika ada hak akses
        'views/examination_views.xml',
        'views/templates.xml',
    ],

    # Data demo, hanya untuk mode demo
    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
