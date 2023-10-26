# -*- coding: utf-8 -*-
import logging
import pprint
from odoo.addons.payment import utils as payment_utils
from werkzeug import urls
from odoo.addons.payment_mollie.const import SUPPORTED_LOCALES
from odoo import _, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    """inherit model of payment transaction"""
    _inherit = 'payment.transaction'

    def _msp_prepare_payment_request_payload(self):
        """ Create the payload for the payment request based on the transaction values.

        :return: The request payload
        :rtype: dict
        """
        user_lang = self.env.context.get('lang')
        base_url = self.provider_id.get_base_url()
        converted_amount = payment_utils.to_minor_currency_units(self.amount,
                                                                         self.currency_id)
        return {
            "order_id":  self.reference,
            "currency": self.currency_id.name,
            "amount": str(converted_amount),
            'language': self.partner_lang[:2],
            "description": "Test Order Description",
            "payment_options": {
                "notification_url": "https://testmerchant.multisafepay.com/transaction-notifications",
                "notification_method": "POST",
                'redirect_url': urls.url_join(
                    base_url, '/shop/payment/msp'),
                "cancel_url": urls.url_join(
                    base_url, '/payment/multisafepay/notify?type=cancel'),
                "return_url": "/shop/payment/msp",
                "close_window": True
            },
            'locale': user_lang if user_lang in SUPPORTED_LOCALES else 'en_US',
        }

    def _get_specific_rendering_values(self, processing_values):
        """ Override of payment to return multi safe pay-specific rendering values.

        Note: self.ensure_one() from `_get_processing_values`

        :param dict processing_values: The generic and specific processing values of the transaction
        :return: The dict of provider-specific rendering values
        :rtype: dict
        """
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'multi_safe_pay':
            return res
        payload = self._msp_prepare_payment_request_payload()
        _logger.info("sending '/payments' request for link creation:\n%s", pprint.pformat(payload))
        payment_data = self.provider_id._msp_make_request('/orders', data=payload)
        self.provider_reference = payment_data.get('id')
        checkout_url = payment_data['data']['payment_url']
        parsed_url = urls.url_parse(checkout_url)
        url_params = urls.url_decode(parsed_url.query)
        return {'api_url': checkout_url, 'url_params': url_params}

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """ Override of payment to find the transaction based on multisafepay data.

        :param str provider_code: The code of the provider that handled the transaction
        :param dict notification_data: The notification data sent by the provider
        :return: The transaction if found
        :rtype: recordset of `payment.transaction`
        :raise: ValidationError if the data match no transaction
        """
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'multi_safe_pay' or len(tx) == 1:
            return tx

        tx = self.search(
            [('reference', '=', notification_data.get('transactionid')), ('provider_code', '=', 'multi_safe_pay')]
        )
        if not tx:
            raise ValidationError("multi_safe_pay: " + _(
                "No transaction found matching reference %s.", notification_data.get('ref')
            ))
        return tx
