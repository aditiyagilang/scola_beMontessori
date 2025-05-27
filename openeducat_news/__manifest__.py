{
    'name': 'OpenEduCat News',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Manage News for OpenEduCat',
    'description': 'Module to manage news with multiple images and configurable types.',
    'author': 'Your Name',
    'depends': ['base', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/news_type_views.xml',
        'views/op_news_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
