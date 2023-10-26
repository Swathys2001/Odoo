# -*- coding: utf-8 -*-
import geocoder
import requests
from odoo import http


class WeatherNotification(http.Controller):
    """controller for fetching weather data"""

    @http.route('/weather/notification/check', type='json', auth="public",
                methods=['POST'])
    def weather_notification(self):
        """method for fetching weather data"""
        api_key = "1152c32f0ad899921b273ea2eaa9c554";
        g_coder = geocoder.ip('me')
        if g_coder.status_code == 200:
            lat = round(g_coder.latlng[0], 2)
            lng = round(g_coder.latlng[1], 2)
            url = 'https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s' % (
                lat, lng, api_key)
            weather = requests.get(url)
            if weather.status_code == 200:
                weather_data = weather.json()
                return weather_data
            else:
                weather_data = {'data': False}
                return weather_data
