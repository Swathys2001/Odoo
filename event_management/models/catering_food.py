# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EventCateringFood(models.Model):
    """This class is used for showing tree views under each page in catering"""
    _name = "catering.food"
    _description = "Event catering food details"

    welcome_drink_id = fields.Many2one("event.catering", string="catering")
    break_fast_id = fields.Many2one("event.catering", string="catering")
    lunch_id = fields.Many2one("event.catering", string="catering")
    dinner_id = fields.Many2one("event.catering", string="catering")
    snacks_id = fields.Many2one("event.catering", string="catering")
    beverage_id = fields.Many2one("event.catering", string="catering")
    item_id = fields.Many2one("catering.menu", string="Item name")
    description = fields.Char(required=True, string="Description",
                              related="item_id.name")
    quantity = fields.Integer(string="Quantity", default=1)
    uom = fields.Many2one('uom.uom', string='Unit of Measure',
                          related="item_id.uom_id", store=True)
    unit_price = fields.Float(string="Unit Price",
                              currency_field="currency_id",
                              related="item_id.unit_of_price", store=True)
    subtotal = fields.Float(compute="_compute_subtotal",
                            string="Subtotal", store=True)
    company_id = fields.Many2one("res.company",
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one("res.currency",
                                  related="company_id.currency_id")

    @api.depends("quantity", "unit_price")
    def _compute_subtotal(self):
        """compute subtotal based on quantity and unit price"""
        for record in self:
            record.subtotal = record.unit_price * record.quantity
            if record.item_id.category == 'Welcome_drink':
                record.welcome_drink_id.event_id.catering_food_id = record.id
            if record.item_id.category == 'Breakfast':
                record.break_fast_id.event_id.catering_food_id = record.id
            if record.item_id.category == 'Lunch':
                record.lunch_id.event_id.catering_food_id = record.id
            if record.item_id.category == 'Dinner':
                record.dinner_id.event_id.catering_food_id = record.id
            if record.item_id.category == 'Snacks_and_drinks':
                record.snacks_id.event_id.catering_food_id = record.id
            if record.item_id.category == 'Beverages':
                record.beverage_id.event_id.catering_food_id = record.id


