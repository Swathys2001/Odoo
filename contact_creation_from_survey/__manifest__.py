# -*- coding: utf-8 -*-
{
    'name': 'Contact creation from survey',
    'version': '16.0.1.0.0',
    'category': 'Marketing/Contact creation from survey',
    'summary': 'create a new contact when completing the survey',
    'description': 'Contact creation from survey',
    'depends': ['survey'],
    'data': [
         'security/ir.model.access.csv',
         'views/survey_survey.xml',
         'views/contact_creation.xml',
    ],
    'License': 'LGPL-3',
    'installable': True,
    'application': True,
}