# -*- coding: utf-8 -*-
from odoo import models


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        """super this function and append the spanish name into product"""
        result = super()._loader_params_product_product()
        result['search_params']['fields'].append('spanish_name')
        return result
