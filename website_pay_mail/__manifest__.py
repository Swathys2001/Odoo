# -*- coding: utf-8 -*-
{
    'name': 'Website pay mail',
    'depends': ['website', 'mail', 'sale'],
    'version': '16.0.1.0.0',
    'category': 'Website/website_pay_mail',
    'summary': 'send an email to know shopping details of a customer',
    'description': 'Website pay mail',
    'data': [
         'security/sale_manager_group.xml',
         'data/custom_mail.xml',
    ],
    'License': 'LGPL-3',
    'installable': True,
    'application': True,
}