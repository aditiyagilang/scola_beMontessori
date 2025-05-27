{
    'name': 'Attendance Staff',
    'version': '1.0',
    'summary': 'Staff Attendance Management',
    'author': 'Your Company',
    'category': 'Human Resources',
    'depends': ['base', 'openeducat_attendance'],  
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml', 
        'views/attendance_config_views.xml', 
        'views/op_attendance_permission_views.xml', 
        'views/action.xml', 
        'views/attendance_staff_menu.xml', 
    ],
    'installable': True,
    'application': True,
}
