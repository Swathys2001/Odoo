# -*- coding: utf-8 -*-
from odoo import fields, models


class EventManagementConfiguration(models.Model):
    """This class is used for collecting event management configuration"""
    _name = "event.management.config"
    _description = "Event Management Configuration"

    name = fields.Char(string="Name", required=True)
    responsible_person_id = fields.Many2one("res.users",
                                            string="Responsible person",
                                            copy=False)
    notes = fields.Char(string="Notes")
    other_ids = fields.One2many("event.management.config.other.info",
                                'catering_id', string="Others")
