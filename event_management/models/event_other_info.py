# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EventManagementConfig(models.Model):
    """This class is used for collecting event management configuration
     - other info details , Here we can see Total amount and currency symbol
     when add a line in the tree view"""
    _name = "event.management.config.other.info"
    _description = "Event Management Configuration other info"

    name = fields.Char(string="name")
    catering_id = fields.Many2one("event.management.config", string="catering")

    description = fields.Char(required=True, string="Description")
    quantity = fields.Integer(string="Quantity")
    unit_price = fields.Monetary(string="Unit Price",
                                 currency_field="currency_id")
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
