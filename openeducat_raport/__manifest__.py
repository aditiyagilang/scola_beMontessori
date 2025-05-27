# -*- coding: utf-8 -*-
{
    'name': "openeducat_raport",
    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'openeducat_classroom', 'openeducat_core'],

    'data': [
        'security/ir.model.access.csv',
        'views/raport_type.xml',
        'views/raport_criteria.xml',
        'views/raport_achievement.xml',
        'views/raport_views.xml',
        'views/exam_type.xml',
        'views/raport_menu.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],
}

