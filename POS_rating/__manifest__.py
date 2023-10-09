# -*- coding: utf-8 -*-
{
    'name': 'POS Rating',
    'depends': ['point_of_sale'],
    'version': '16.0.1.0.0',
    'category': 'Sales/POS Rating',
    'summary': 'display the rating of a product',
    'description': 'POS Rating',
    'data': [
        'views/product_product.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
         'POS_rating/static/src/js/pos_receipt.js',
         'POS_rating/static/src/xml/pos_view.xml',
         'POS_rating/static/src/xml/pos_receipt_rating.xml',
        ]
    },
    'License': 'LGPL-3',
    'installable': True,
    'application': True,

}