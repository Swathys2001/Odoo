# -*- coding: utf-8 -*-
{
    'name': 'Event Management',
    'version': '16.0.1.0.0',
    'category': 'Service/Event Management',
    'summary': 'To provide event management service',
    'description': 'Event Management',
    'depends': ['mail', 'sale', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/default_data.xml',
        'data/expired_cron.xml',
        # 'views/snippet_template.xml',
        'views/carousel_first.xml',
        'views/event_view_form.xml',
        'views/website_online_template.xml',
        'views/successful_booking.xml',
        'views/show_booking.xml',
        'views/event_types_view.xml',
        'views/event_catering_view.xml',
        'views/catering_food.xml',
        'views/event_booking_view.xml',
        'views/event_config_view.xml',
        'views/catering_menu_view.xml',
        'views/other_info_view.xml',
        'wizard/reporting.xml',
        'report/event_report.xml',
        'report/template.xml',
        'views/event_mgmt_menu.xml',
        'views/website_menu.xml',
    ],
    'assets':  {
        'web.assets_backend': [
            'event_management/static/src/js/action_manager.js',

        ],
        'web.assets_frontend': [
            'event_management/static/src/js/event_booking.js',
            # 'event_management/static/src/js/snippet.js',
            'event_management/static/src/xml/carousel_snippet.xml',
            'event_management/static/src/js/carousel.js',
        ]
    },
    'License': 'LGPL-3',
    'installable': True,
    'application': True,

}
