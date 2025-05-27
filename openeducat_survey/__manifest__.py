{
    'name': 'OpenEduCat Survey Custom',
    'version': '1.0',
    'author': 'Your Name',
    'depends': ['base', 'openeducat_core', 'survey'], 

    'data': [
        'views/survey_user_input_view_form.xml',
        'views/questions_max_score.xml',
        'views/survey_user_input_edit_view.xml',  
        'views/survey_form_inherit.xml',
    ],

    'models': [
        'models/survey_survey.py',
        'models/survey_user_input.py',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
