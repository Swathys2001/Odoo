# -*- coding: utf-8 -*-
from odoo import api, models


class SaleOrder(models.Model):
    """inherit sale order"""
    _inherit = 'sale.order'

    def action_send_email(self, order):
        """send an email have the details about sale order, customer,
         order lines and total amount"""
        list1 = []
        groups = self.env['res.groups'].search([
            ('name', '=', 'Manager')])
        for rec in groups:
            for user in rec.users:
                list1.append(user.email)
                from_mail = self.env.user.email
                mail_template = (self.env.ref(
                    'website_pay_mail.email_template_shopping'))
                email_values = {'email_from': from_mail,
                                'email_to': list1[0],
                                'email_cc': list1[1:],
                                'subject': mail_template.subject
                                }
                mail_template.send_mail(order.id, email_values=email_values,
                                        force_send=True)


