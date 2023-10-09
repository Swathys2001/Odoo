# -*- coding: utf-8 -*-
from odoo import fields, models


class CateringMenu(models.Model):
    """This class is used for catering menu - here we can set name, category,
    image, unit price and unit of measure"""
    _name = "catering.menu"
    _description = "Catering menu"

    name = fields.Char(string="Name", required=True)
    menu_id = fields.Many2one("event.catering", string="menu")
    category = fields.Selection(selection=[("Welcome_drink", "Welcome drink"),
                                           ("Breakfast", "Break fast"),
                                           ("Lunch", "Lunch"),
                                           ("Dinner", "Dinner"),
                                           ("Snacks_and_drinks",
                                            "Snacks and drinks"),
                                           ("Beverages", "Beverages")],
                                string="Category", required=True)
    image = fields.Binary(string="Image")
    unit_of_price = fields.Float(string="Unit of Price", required=True)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
