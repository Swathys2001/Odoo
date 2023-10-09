# -*- coding: utf-8 -*-
from odoo import api, fields, models
from deep_translator import GoogleTranslator


class ProductProduct(models.Model):
    """inherit the class of product_product"""
    _inherit = 'product.product'

    spanish_name = fields.Char(string="Spanish name",
                               compute="compute_spanish_name", store=True)

    @api.depends('name')
    def compute_spanish_name(self):
        """used to find spanish name of a product"""
        for rec in self:
            to_translate = rec.name
            translated = GoogleTranslator(source='auto', target='de').translate(
                to_translate)
            rec.spanish_name = translated

