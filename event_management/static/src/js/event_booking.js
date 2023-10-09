odoo.define('event_management.event_booking_js', function (require) {
    'use strict';
    var rpc = require('web.rpc');
    var publicWidget = require('web.public.widget');
    publicWidget.registry.EventBookingWidget = publicWidget.Widget.extend({
        selector: '#table_view',
        events: {
            'click .btn-primary': 'onClickButton',
        },
        onClickButton: function (ev) {
            var recordId = $(ev.currentTarget).data('record-id');
            rpc.query({
                route: '/event_booking_details/change_state',
                params: {
                    'record': recordId
                },
            }).then(function () {
                location.reload();
            });
        },
      })
    });