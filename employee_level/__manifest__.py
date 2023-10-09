# -*- coding: utf-8 -*-
{
    'name': 'Employee Level',
    'version': '16.0.1.0.0',
    'category': 'Human Resources/Employee level',
    'summary': 'To set employee level',
    'description': 'Employee level',
    'depends': ['hr'],
    'data': [
         'security/ir.model.access.csv',
         'data/default_data.xml',
         'views/hr_employee.xml',
         'views/employee_level.xml',
    ],
    'License': 'LGPL-3',
    'installable': True,
    'application': True,
}