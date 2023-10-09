
odoo.define('dynamic_snippet_blog.dynamic', function (require) {
   var PublicWidget = require('web.public.widget');
   var rpc = require('web.rpc');
   console.log(345)
   var Dynamic = PublicWidget.Widget.extend({
       selector: '.event_view',
       start: function () {
           var self = this;
           rpc.query({
                route:'/event_view',
                params:{},
                }).then(function (result) {
                href = '/event_view/form'
               result.forEach(function(demo){
                image = 'data:image/png;base64,' + demo['event_img']
                self.$('.card-group').append(`<div class="card col-lg-5 m-4" style="width:19rem;">
                                                <div class="card-body">
                                                <a href="/event_view_form/${demo['id']}">View details</a>
                                                <img src="${image}" class="card-img-top" alt="image"/>
                                                <h4 class="card-text"><i><b>${demo['event_name']}</b></i><br/>
                                                </h4><i><p class="card-text">Customer:${demo['customer']}</p><br/>
                                                <p class="card-text">From:${demo['event_start_date']}</p><br/>
                                                <p class="card-text">To:${demo['event_end_date']}</p></i>
                                                </div></div>`)
                });
            })
}
   })

   PublicWidget.registry.dynamic_snippet_blog = Dynamic;
   return Dynamic;
});
