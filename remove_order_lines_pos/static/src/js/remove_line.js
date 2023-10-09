/**@odoo-module **/
   import Orderline from 'point_of_sale.Orderline';
   import Registries  from 'point_of_sale.Registries';
   const RemoveLine = (Orderline) => class RemoveLine extends Orderline {
        ClearSingleLine(){
              this.env.pos.get_order().remove_orderline(this.props.line)
          }
   }
    Registries.Component.extend(Orderline, RemoveLine);