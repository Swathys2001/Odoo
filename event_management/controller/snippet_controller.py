from odoo import http
from odoo.http import request


class SnippetView(http.Controller):
    @http.route(['/event_view'], type="json", auth="public")
    def event_view(self):
        events = (request.env['event.management.booking'].sudo().
                  search([], order='booking_date desc', limit=4))
        events_data = [{'id': record.id,
                        'event_name': record.event_type_id.name,
                       'customer': record.customer_id.name,
                        'booking_date': record.booking_date,
                        'event_start_date': record.event_start_date,
                        'event_end_date': record.event_end_date,
                        'event_img': record.image}
                       for record in events]
        return events_data

    @http.route(['/event_view_carousel'], type="json", auth="public",
                website=True, methods=['POST'])
    def event_view(self):
        events = (request.env['event.management.booking'].sudo().
                  search([], order='booking_date desc',limit=10))
        events_data = [{'id': record.id,
                        'event_name': record.event_type_id.name,
                        'customer': record.customer_id.name,
                        'booking_date': record.booking_date,
                        'event_start_date': record.event_start_date,
                        'event_end_date': record.event_end_date,
                        'event_img': record.image}
                       for record in events]
        return events_data

    @http.route('/event_view_form/<int:id>', type='http',
                auth="public", website=True)
    def event_view_form(self, **kwargs):
        """used to change state in website and backend"""
        events_data = (request.env['event.management.booking'].sudo().
                       browse(kwargs['id']))
        values = {
            'events': events_data,
        }
        return request.render('event_management.event_form', values)
