# -*- coding: utf-8 -*-
{
    'name': 'Multisafepay Integration',
    'version': '16.0.1.0.0',
    'category': 'Accounting/Multi safe pay',
    'summary': 'Create a new payment provider',
    'description': 'Multisafepay Integration',
    'depends': ['base','payment'],
    'data': [
        'views/payment_template.xml',
        'data/payment_provider_msp.xml',
        'views/payment_provider.xml',
    ],
    'License': 'LGPL-3',
    'installable': True,
    'application': True,
}
