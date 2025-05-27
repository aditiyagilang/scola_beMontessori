{
    'name': 'Custom Class Configuration',
    'version': '1.0',
    'category': 'Education',
    'summary': 'Custom module for class configuration',
    'description': 'Module to manage and configure classes in OpenEduCat.',
    'author': 'Laila',
    'depends': ['base', 'openeducat_core'],
    'data': [
        'security/ir.model.access.csv',
        'views/class_config_view.xml',
    ],
    'installable': True,
    'application': True,
}