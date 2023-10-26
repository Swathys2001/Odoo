# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale, TableCompute


class WebsiteSaleInherit(WebsiteSale):
    """supering function of shop_payment_confirmation"""
    @http.route(['/shop/confirmation'], type='http', auth="public",
                website=True, sitemap=False)
    def shop_payment_confirmation(self, **post):
        """ Payment step. This page proposes several payment means based on available
        payment.provider. State at this point :

         - a draft sales order with lines; otherwise, clean context / session and
           back to the shop
         - no transaction in context / session, or only a draft one, if the customer
           did go to a payment.provider website but closed the tab without
           paying / canceling
        """
        payment_super = super(WebsiteSaleInherit, self).shop_payment_confirmation()
        sale_order_id = request.session.get('sale_last_order_id')
        if sale_order_id:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            request.env['sale.order'].action_send_email(order)
        return payment_super


