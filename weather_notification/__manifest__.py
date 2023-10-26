# -*- coding: utf-8 -*-
{
    'name': 'Weather notification',
    'version': '16.0.1.0.0',
    'category': 'Services/Weather notification',
    'summary': 'To provide current weather details',
    'description': 'Weather notification',
    'depends': ['web', 'base'],
    'version': '16.0.1.0.0',
    "assets": {
        'web.assets_backend':
            [
                "weather_notification/static/src/js/weather_notification.js",
                "weather_notification/static/src/xml/weather_notification_templates.xml",
                "weather_notification/static/src/scss/weather.scss",
        ]
    },
    'external_dependencies': {
        'python': ['geocoder'],
    },
    'License': 'LGPL-3',
    'installable': True,
    'application': True,
}