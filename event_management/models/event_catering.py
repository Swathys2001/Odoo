# -*- coding: utf-8 -*-
from odoo import api, fields, models, exceptions


class Catering(models.Model):
    """This class is used for collecting details about catering - here we can
    set all fields, when a boolean field is true then show a new page -
     calculates each page total and grand total """
    _name = "event.catering"
    _description = "Event Management Catering"

    name = fields.Char(required=True, readonly=True,
                       default=lambda self: 'New', string="Name", copy=False)
    event_id = fields.Many2one("event.management.booking", string="Event type",
                               required=True, copy=False,
                               domain=[('catering_id', '=', False)])
    booking_date = fields.Date(string="Event Date",
                                   related="event_id.booking_date")
    event_start_date = fields.Date(string="Event Start Date",
                                       related="event_id.event_start_date")
    event_end_date = fields.Date(string="Event End Date",
                                     related="event_id.event_end_date")
    guests = fields.Integer(string="Guests", default=1)
    welcome_drink = fields.Boolean(string="Welcome drink")
    break_fast = fields.Boolean(string="Break fast")
    lunch = fields.Boolean(string="Lunch")
    dinner = fields.Boolean(string="Dinner")
    snacks = fields.Boolean(string="Snacks and Drinks")
    beverages = fields.Boolean(string="Beverages")
    new_notes = fields.Char()
    welcome_drink_ids = fields.One2many("catering.food",
                                        'welcome_drink_id',
                                        string="welcome_drink")
    catering_menu_ids = fields.One2many("catering.menu", "menu_id")
    break_fast_ids = fields.One2many("catering.food",
                                     'break_fast_id', string="break_fast")
    lunch_ids = fields.One2many("catering.food",
                                'lunch_id', string="lunch")
    dinner_ids = fields.One2many("catering.food",
                                 'dinner_id', string="dinner")
    snacks_ids = fields.One2many("catering.food",
                                 'snacks_id', string="snacks")
    beverages_ids = fields.One2many("catering.food",
                                    'beverage_id', string="beverages")
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('delivered', 'Delivered'),
                              ('invoiced', 'Invoiced'),
                              ('expired', 'Expired')], string="State",
                             readonly=True, default="draft")
    company_id = fields.Many2one("res.company",
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one("res.currency",
                                  related="company_id.currency_id")
    welcome_drink_total = fields.Monetary(string="Total:", readonly=True,
                                          compute="_compute_welcome_drink_total",
                                          currency_field="currency_id")
    break_fast_total = fields.Monetary(string="Total :", readonly=True,
                                       compute="_compute_break_fast_total",
                                       currency_field="currency_id")
    lunch_total = fields.Monetary(string="Total :", readonly=True,
                                  compute="_compute_lunch_total",
                                  currency_field="currency_id")
    dinner_total = fields.Monetary(string="Total :", readonly=True,
                                   compute="_compute_dinner_total",
                                   currency_field="currency_id")
    snacks_total = fields.Monetary(string="Total :", readonly=True,
                                   compute="_compute_snacks_total",
                                   currency_field="currency_id")
    beverages_total = fields.Monetary(string="Total :", readonly=True,
                                      compute="_compute_beverages_total",
                                      currency_field="currency_id")
    grand_total = fields.Monetary(string="Grand total :", readonly=True,
                                  compute="_compute_grand_total",
                                  currency_field="currency_id", store=True)
    booking_ids = fields.One2many("event.management.booking", "catering_id")
    invoice_ribbon = fields.Boolean(default=False, compute="compute_ribbon",
                                    store=True)

    @api.model
    def create(self, vals):
        """This function used for creating sequence for event catering"""
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'catering.sequence') or 'New'
        res = super(Catering, self).create(vals)
        return res

    @api.onchange("event_start_date")
    def _onchange_event_start_date(self):
        """Here start date is over then change the state to expired"""
        if self.event_start_date < self.booking_date:
            self.state = 'expired'

    @api.depends("welcome_drink_total")
    def _compute_welcome_drink_total(self):
        """Used to calculate welcome drink page total"""
        for record in self:
            if record.welcome_drink_ids:
                total_list = record.welcome_drink_ids.mapped(
                    lambda self: self.subtotal)
                total_sum = sum(total_list)
                record.welcome_drink_total = total_sum
            else:
                record.welcome_drink_total = 0.0

    def _compute_break_fast_total(self):
        """Used to calculate break fast page total"""
        for record in self:
            if record.break_fast_ids:
                total_list = record.break_fast_ids.mapped(
                    lambda self: self.subtotal)
                total_sum = sum(total_list)
                record.break_fast_total = total_sum
            else:
                record.break_fast_total = 0.0

    def _compute_lunch_total(self):
        """Used to calculate lunch page total"""
        for record in self:
            if record.lunch_ids:
                total_list = record.lunch_ids.mapped(
                    lambda self: self.subtotal)
                total_sum = sum(total_list)
                record.lunch_total = total_sum
            else:
                record.lunch_total = 0.0

    def _compute_dinner_total(self):
        """Used to calculate dinner page total"""
        for record in self:
            if record.dinner_ids:
                total_list = record.dinner_ids.mapped(
                    lambda self: self.subtotal)
                total_sum = sum(total_list)
                record.dinner_total = total_sum
            else:
                record.dinner_total = 0.0

    def _compute_snacks_total(self):
        """Used to calculate snacks page total"""
        for record in self:
            if record.snacks_ids:
                total_list = record.snacks_ids.mapped(
                    lambda self: self.subtotal)
                total_sum = sum(total_list)
                record.snacks_total = total_sum
            else:
                record.snacks_total = 0.0

    def _compute_beverages_total(self):
        """Used to calculate beverages page total"""
        for record in self:
            if record.beverages_ids:
                total_list = record.beverages_ids.mapped(
                    lambda self: self.subtotal)
                total_sum = sum(total_list)
                record.beverages_total = total_sum
            else:
                record.beverages_total = 0.0

    @api.depends("welcome_drink_total","break_fast_total",
                 "lunch_total","dinner_total","snacks_total","beverages_total")
    def _compute_grand_total(self):
        """calculates all totals"""
        for record in self:
            record.grand_total = record.welcome_drink_total +\
                                 record.break_fast_total + \
                                 record.lunch_total + \
                                 record.dinner_total + record.snacks_total + \
                                 record.beverages_total

    def confirm_button(self):
        """confirm button action - change state to confirmed"""
        self.state = 'confirmed'
        for record in self:
            if record.event_id.state == 'confirm':
                record.event_id.catering_id = record.id
            else:
                record.event_id.catering_id = record.id

    def delivery_button(self):
        """delivery button action - change state to delivered"""
        self.state = 'delivered'

    @api.model
    def _expired_cron(self):
        """The function is used for checking start date daily"""
        session_ids = self.env['event.catering'].search(
            [('state', '!=', 'draft')])
        for session in session_ids:
            if session.event_start_date < session.booking_date:
                session.state = 'expired'

    @api.depends("event_id.ribbon")
    def compute_ribbon(self):
        """If payment state is paid then display paid
         ribbon on event catering"""
        for rec in self:
            if rec.event_id.ribbon == True:
                rec.invoice_ribbon = True
            else:
                rec.invoice_ribbon = False
