# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class EventBooking(http.Controller):
    """Used to show event booking details"""
    @http.route(['/event_booking'], type='http', auth="public", website=True)
    def event_booking(self, **post):
        """used to log event booking"""
        events_data = request.env['event.management'].sudo().search([])
        partners = request.env['res.partner'].sudo().search([])
        values = {
            'events': events_data,
            'partners': partners
        }
        return request.render("event_management.event_booking_online", values)

    @http.route(['/event_booking/submit'], type='http', auth="user",
                website=True)
    def survey_form_view(self, **post):
        """when submit button clicks this data will be added to the backend
         and redirect to complete booking page"""
        a = request.env['event.management.booking'].sudo().create({
            'event_type_id': int(post.get('event_type_id')),
            'customer_id': post.get('customer_id'),
            'booking_date': post.get('booking_date'),
            'event_start_date': post.get('event_start_date'),
            'event_end_date': post.get('event_end_date'),
        })
        return request.render("event_management.complete_booking", {})

    @http.route(['/event_booking_details'], type='http', auth="user",
                website=True)
    def show_booking(self):
        """Used to show event booking details when a portal user enters
        then show their own bookings and admin shows all tickets """
        user = request.env.user
        if user.has_group('base.group_user'):
            events = request.env['event.management.booking'].sudo().search([])
            values = {
                'events': events,
            }
            return request.render("event_management.show_booking", values)
        if user.has_group('base.group_portal'):
            events = (request.env['event.management.booking'].sudo().search([]).
                      filtered(lambda a: a.create_uid == user))
            values = {
                'events': events,
            }
            return request.render("event_management.show_booking", values)

    @http.route('/event_booking_details/change_state', type='json',
                auth="public", website=True)
    def change_state(self, record):
        """used to change state in website and backend"""
        (request.env['event.management.booking'].sudo().browse(record).
         booking_confirm_button())








