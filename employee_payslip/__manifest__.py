# -*- coding: utf-8 -*-
{
    'name': 'Employee payslip',
    'version': '16.0.1.0.0',
    'category': 'Accounting/Employee payslip',
    'summary': 'Employees can print their own payslip',
    'description': 'Employee payslip',
    'depends': ['hr_payroll_community', 'base', 'portal'],
    'data': [
        'views/employee_slip.xml',
        'views/portal_my_payslips.xml',
    ],
    'License': 'LGPL-3',
    'installable': True,
    'application': True,
}