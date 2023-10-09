# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductProduct(models.Model):
    """inherit the class of product_product"""
    _inherit = 'product.product'

    rating = fields.Selection(selection=[('1', '1'),
                              ('2', '2'),
                              ('3', '3'),
                              ('4', '4'),
                              ('5', '5')], string="Rating")
