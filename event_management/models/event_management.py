# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EventManagementOtherInfo(models.Model):
    """This class is used for collecting event management details"""
    _name = "event.management"
    _description = "Event Management"

    name = fields.Char(string="Name", required=True)
    event_code = fields.Char(string='Code', required=True, readonly=True,
                             default=lambda self: '000', copy=False)
    event_img = fields.Binary(string="Event image", store=True)

    @api.model
    def create(self, vals):
        """Used to create sequence for event code """
        if vals.get('event_code', '000') == '000':
            vals['event_code'] = self.env['ir.sequence'].next_by_code(
                'event.sequence') or '000'
        res = super(EventManagementOtherInfo, self).create(vals)
        return res
