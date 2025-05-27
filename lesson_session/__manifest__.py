{
    'name': 'Lesson Session',
    'version': '1.0',
    'summary': 'Manage lesson sessions and schedules',
    'description': """
This module allows you to manage lesson sessions and their schedules. 
You can define start and end times for each session.
    """,
    'author': 'Lailatul Rohma, GCG',
    'category': 'Education',
    'data': [
        'security/ir.model.access.csv',
        'views/lesson_session_view.xml',  # File view untuk sesi pelajaran
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}