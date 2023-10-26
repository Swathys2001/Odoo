# -*- coding: utf-8 -*-
{
    'name': 'Attendance Report',
    'version': '16.0.1.0.0',
    'category': 'Human Resources/Attendance report',
    'summary': 'Create attendance report',
    'description': 'Report of attendance',
    'depends': ['hr_attendance'],
    'data': [
       'security/ir.model.access.csv',
       'wizard/attendance_report_wizard.xml',
       'report/attendance_report.xml',
       'report/attendance_report_template.xml',
       'views/hr_attendance_menu.xml',
    ],
    'License': 'LGPL-3',
    'installable': True,
    'application': True,
}
