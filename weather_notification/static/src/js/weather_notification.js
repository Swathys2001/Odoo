odoo.define('weather_systray.weather', function(require) {
  "use strict";
  var core = require('web.core');
  var QWeb = core.qweb;
  var SystrayMenu = require('web.SystrayMenu');
  var Widget = require('web.Widget');
  var rpc = require('web.rpc');
  var WeatherMenu = Widget.extend({
      template: 'user_weather_notification.UserMenuS',
      events: {
          'click #create_so': 'onclick_myicon',
      },
      start: function() {
      var self = this
      self.$('.card').hide();
      },
      /*toggle the card hide or visible*/
      onclick_myicon: async function() {
        if (self.$(".card").is(":visible")) {
            self.$('.card').hide();
        }
        else {
            self.$('.card').show();
            rpc.query({
                    route: "/weather/notification/check",
                }).then(function(result) {
                if (result.data == false){
                self.$("#description").text('Configure Settings')
                }else{
                console.log(result)
                self.$("#title").text(result.name);
                self.$("#main").text(result.weather[0].main);
                var temp = Math.floor(result.main.temp - 273);
                self.$("#temp").text(temp + "°C");
                self.$("#description").text(result.weather[0].description);
                const date = new Date();
                let day = date.getDate();
                let month = date.getMonth() + 1;
                let year = date.getFullYear();
                let currentDate = `${day}-${month}-${year}`;
                 var current_date = new Date();
                 var datetime = "Last update:" + currentDate + " @ "
                + current_date.getHours() + ":"
                + current_date.getMinutes() + ":" + current_date.getSeconds();
                self.$("#last_update").text(datetime);
                }
               })
        }
    }
  });
  SystrayMenu.Items.push(WeatherMenu);
  return WeatherMenu;
});