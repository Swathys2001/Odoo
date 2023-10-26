# -*- coding: utf-8 -*-
import logging
import requests
from werkzeug import urls
from odoo import _, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    """inherit model of payment provider and add fields"""
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('multi_safe_pay', "multi safe pay")],
        ondelete={'multi_safe_pay': 'set default'})
    api_key = fields.Char(string="API Key")

    def _msp_make_request(self, endpoint, data=None, method='POST'):
        """ Make a request at multisafepay endpoint"""
        self.ensure_one()
        endpoint = f'/v1/json/{endpoint.strip("/")}'
        url = urls.url_join('https://testapi.multisafepay.com/', endpoint)
        headers = {
            "Accept": "application/json",
            "api-key": self.api_key,
            "Content-Type": "application/json",
        }
        try:
            response = requests.request(method, url, json=data, headers=headers,
                                        timeout=60)
        except requests.exceptions.RequestException:
            _logger.exception("unable to communicate with MultiSafePay: %s",
                              url)
            raise ValidationError("MultiSafePay: " + _(
                "Could not establish the connection to the API."))
        return response.json()


