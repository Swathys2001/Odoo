odoo.define('spanish_product.spanish_product_name', function(require) {
'use strict';
   var { Orderline } = require('point_of_sale.models');
   const Registries = require('point_of_sale.Registries');
   const customOrder = (Orderline) => class PosSaleOrderline extends Orderline {
    export_for_printing() {
       var result = super.export_for_printing(...arguments)
       result.rating = this.get_product().rating
       return result;
   }
   }
    Registries.Model.extend(Orderline, customOrder);
});
