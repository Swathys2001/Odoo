# -*- coding: utf-8 -*-
{
    'name': 'Spanish product name in POS',
    'depends': ['point_of_sale'],
    'version': '16.0.1.0.0',
    'category': 'Sales/Spanish product name in POS',
    'summary': 'display the spanish name under product name',
    'description': 'Spanish product name in POS',
    'data': [
        'views/product_product.xml',
    ],
    'assets': {
     'point_of_sale.assets': [
        'spanish_product_name/static/src/js/pos_session.js',
        'spanish_product_name/static/src/xml/pos_session.xml',
        'spanish_product_name/static/src/xml/pos_session_receipt.xml',

      ]
    },
    'License': 'LGPL-3',
    'installable': True,
    'application': True,
}
