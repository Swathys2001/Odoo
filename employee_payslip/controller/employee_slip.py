# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request


class PortalAccount(CustomerPortal):
    """Inherit customer portal and add a new menu payslip"""
    def _prepare_home_portal_values(self, counters):
       values = super()._prepare_home_portal_values(counters)
       user = request.env.user.employee_id.id
       if 'payslip_count' in counters:
           payslip_count = request.env['hr.payslip'].search_count(
               [('employee_id', '=', user)]) if request.env['hr.payslip'].check_access_rights('read',
                                                                  raise_exception=False) else 0
           values['payslip_count'] = payslip_count
       return values

    @http.route(['/my/payslips', '/my/payslip/page/<int:page>'], type='http',
                auth="user", website=True)
    def portal_my_payslips(self, **kw):
        """Payslip menu redirect to a new page and show the payslip details"""
        user = request.env.user.employee_id.id
        payslip_data = request.env['hr.payslip'].sudo().search([
            ('employee_id', '=', user)
        ])
        values = {
           'payslip_data': payslip_data
        }
        return request.render("employee_payslip.portal_my_payslips", values)

    @http.route(['/report/pdf/hr_payslip.report_payslipdetails/<int:id>'],
                methods=['POST', 'GET'], csrf=False, type='http', auth="user",
                website=True)
    def print_id(self, **kw):
        id = kw['id']
        if id:
            pdf, _ = request.env.ref(
                'hr_payroll_community.report_payslipdetails').sudo().render_qweb_pdf([id])
            pdfhttpheaders = [('Content-Type', 'application/pdf'),
                              ('Content-Length', len(pdf))]
            return request.make_response(pdf, headers=pdfhttpheaders)
        else:
            return request.redirect('/')


