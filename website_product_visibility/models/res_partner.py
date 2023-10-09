# -*- coding: utf-8 -*-
from odoo import models, fields


class ResPartner(models.Model):
    """Inherit model of res_partner and add 2 fields"""
    _inherit = ['res.partner']

    allowed_product_ids = fields.Many2many('product.template')
    allowed_product_category_ids = fields.Many2many('product.public.category')

