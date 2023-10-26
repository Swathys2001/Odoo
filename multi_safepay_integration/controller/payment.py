# -*- coding: utf-8 -*-
from odoo.http import Controller, request, route


class MpsPayment(Controller):
    """redirect page to payment status"""
    _return_url = '/payment/msp/return'

    @route(route=['/shop/payment/msp'], auth="public", type="http", website=True,
           methods=['GET'])
    def msp_payment(self, **data):
        """page redirect to payment status"""
        tx_sudo = request.env['payment.transaction'].sudo()._get_tx_from_notification_data(
            'multi_safe_pay', data
        )
        tx_sudo.provider_reference = 'multi_safe_pay' + tx_sudo.reference
        payment_data = tx_sudo.provider_id._msp_make_request(
                    f'/orders/{tx_sudo.reference}', method="GET"
                )
        if payment_data['data']['status'] == 'completed':
            tx_sudo._set_done()
        return request.redirect('/payment/status')
