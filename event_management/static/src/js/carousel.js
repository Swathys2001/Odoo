odoo.define('event_view_snippet.snippet', function(require) {
'use strict';
var PublicWidget = require('web.public.widget');
var rpc = require('web.rpc');
var core = require('web.core');
var qweb = core.qweb;
var Dynamic = PublicWidget.Widget.extend({
    selector: '.dynamic_snippet_blog',
    willStart: async function() {
            var self = this;
            await rpc.query({
            route: '/event_view_carousel',
            }).then((data) => {
            this.data = data;
    })
    },
    start: function() {
        var chunks = _.chunk(this.data, 4)
        console.log(chunks)
        chunks[0].is_active = true
        this.$el.find('#carousel').html(
        qweb.render('event_management.event_carousels', {
        chunks
    })
    )
    },
})
PublicWidget.registry.dynamic_snippet_blog = Dynamic;
return Dynamic;
});