/**@odoo-module **/
  const PosComponent = require('point_of_sale.PosComponent');
  const ProductScreen = require('point_of_sale.ProductScreen');
  const { useListener } = require("@web/core/utils/hooks");
  const Registries = require('point_of_sale.Registries');
  const PaymentScreen = require('point_of_sale.PaymentScreen');
  class CustomDemoButtons extends PosComponent {
      setup() {
          super.setup();
          useListener('click', this.ClearAll);
      }
      ClearAll() {
               var current_order = this.env.pos.get_order();
               var order_lines = current_order.orderlines.slice()
               for (const orderLine of order_lines) {
                  console.log(orderLine)
                  current_order.remove_orderline(orderLine)
               }
          }
      }
    CustomDemoButtons.template = 'CustomDemoButtons';
      ProductScreen.addControlButton({
          component: CustomDemoButtons,
          position: ["after", "OrderlineCustomerNoteButton"],
          condition: function() {
              return this.env.pos;
          },
      });
      Registries.Component.add(CustomDemoButtons);
      return CustomDemoButtons;
})