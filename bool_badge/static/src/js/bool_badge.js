/**@odoo-module **/
import {registry} from "@web/core/registry"
const { Component } = owl
import { standardFieldProps } from "@web/views/fields/standard_field_props";

class BoolBadge extends Component{
    setup(){
        const options = this.props.options || {}
        this.trueValue = options.trueValue || "Yes"
        this.trueColor = options.trueColor || "green"
        this.falseValue = options.falseValue || "No"
        this.falseColor = options.falseColor || "red"
        this.defaultColor = options.defaultColor || "white"
    }
    updateValue(val){
      this.props.update(val)
    }

}
BoolBadge.template="BoolBadge"
BoolBadge.props = {
         ...standardFieldProps,
         options:
         {
          type: Object,
          optional:true
          }
}
BoolBadge.supportedTypes = ['boolean']
BoolBadge.extractProps = ({attrs}) =>{
      return {options: attrs.options}
}

registry.category('fields').add("bool_badge", BoolBadge)
