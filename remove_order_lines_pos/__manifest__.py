# -*- coding: utf-8 -*-
{
    'name': 'Remove order lines in POS',
    'depends': ['point_of_sale'],
    'version': '16.0.1.0.0',
    'category': 'Sales/Remove order lines in POS',
    'summary': 'Clear button to remove order lines',
    'description': 'Remove order lines in POS',
    'assets': {
        'point_of_sale.assets': [
            'remove_order_lines_pos/static/src/js/clear_button.js',
            'remove_order_lines_pos/static/src/js/remove_line.js',
            'remove_order_lines_pos/static/src/xml/remove_lines.xml',
            'remove_order_lines_pos/static/src/xml/remove_single_line.xml',

        ]
    },
    'License': 'LGPL-3',
    'installable': True,
    'application': True,
}