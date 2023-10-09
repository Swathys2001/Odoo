# -*- coding: utf-8 -*-
from dateutil import relativedelta
from odoo import api, fields, models, exceptions
from odoo import Command


class EventManagementBooking(models.Model):
    """This class is used for collecting event booking details - automatically
     generate a name by concatenating customer name, event type , start date,
     end date and calculates duration """
    _name = "event.management.booking"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Event Management Booking"

    name = fields.Char(default="New", compute="_compute_name", string="Name",
                       copy=False)
    event_type_id = fields.Many2one("event.management", string="Event Type",
                                    copy=False, required=True)
    image = fields.Binary(string="image",
                          related="event_type_id.event_img",
                          store=True)
    customer_id = fields.Many2one("res.partner", required=True,
                                  string="Customer name", copy=False)
    booking_date = fields.Date(default=fields.Date.today(),
                               readonly=True, string="Booking date")
    event_start_date = fields.Date(
        required=True, string="Event start date",
        default=fields.date.today() + relativedelta.relativedelta(days=2))
    event_end_date = fields.Date(
        required=True, string="Event end date",
        default=fields.date.today() + relativedelta.relativedelta(days=10))
    duration = fields.Integer(readonly=True, string="Duration", compute="compute_event_end_date")
    catering_ids = fields.One2many("event.catering", 'event_id',
                                   string="catering")
    catering_id = fields.Many2one("event.catering", string="catering")
    catering_food_id = fields.Many2one("catering.food", string="Catering food")
    state = fields.Selection(selection=[('draft', 'Draft'),
                                        ('confirm', 'Confirm'),
                                        ('invoice', 'invoice')], readonly=True,
                             default="draft")
    invoice_id = fields.Many2one("account.move", string="invoice")
    ribbon = fields.Boolean(default=False, compute="_compute_ribbon",
                            store=True)

    @api.depends("event_end_date", "event_start_date")
    def compute_event_end_date(self):
        """Here the start and end date difference is calculated for duration"""
        if self.event_start_date:
            if self.event_end_date:
                if self.event_start_date == self.event_end_date:
                    self.duration = 1
                else:
                    diff = (self.event_end_date - self.event_start_date).days
                    if diff < 1:
                        self.event_start_date = fields.datetime.today() + \
                            relativedelta.relativedelta(days=2)
                        self.event_end_date = fields.datetime.today() + \
                            relativedelta.relativedelta(days=10)
                        raise exceptions.ValidationError(
                            "Invalid dates")
                    self.duration = diff

    @api.depends("event_type_id", "customer_id",
                 "event_end_date", "event_start_date")
    def _compute_name(self):
        """concatenate event type, customer name, start date and
        end date for name creation"""
        self.name="New"
        for record in self:
            if record.event_type_id and record.customer_id and record.event_start_date and record.event_end_date:
                record.name = str(record.event_type_id.name or '') + ":" +\
                                  str(record.customer_id.name or '') + "/" +\
                                  str(record.event_start_date or '') + ":" +\
                                  str(record.event_end_date or '')

    def catering_service(self):
        """button action - When clicking this button it will redirect to
        event catering page"""
        return {
            'name': 'event catering',
            'type': 'ir.actions.act_window',
            'res_model': 'event.catering',
            'view_mode': 'form',
            'context': {'default_event_id': self.id},
        }

    def booking_confirm_button(self):
        """ booking confirm button action - when clicking confirm button in
        event booking also change the state to confirm in catering page"""
        self.state = 'confirm'
        for record in self:
            if record.catering_ids:
                for r in record.catering_ids:
                    r.state = 'confirmed'

    def catering_service_button(self):
        """smart button action - used to show tree view of catering"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Catering',
            'view_mode': 'tree,form',
            'res_model': 'event.catering',
            'context': "{'create':False}"
        }

    def create_invoice(self):
        """button action - To create invoice"""
        self.state = 'invoice'
        self.catering_id.state = 'invoiced'
        vals = []
        search = self.env['event.catering'].search([('event_id', '=', self.id)])
        for rec in search.welcome_drink_ids:
            vals.append((Command.create(
                         {
                             'name': rec.item_id.name,
                             'quantity': rec.quantity,
                             'price_unit': rec.unit_price,
                             'price_subtotal': rec.subtotal
                         })))
        for rec in search.break_fast_ids:
            vals.append((Command.create(
                         {
                             'name': rec.item_id.name,
                             'quantity': rec.quantity,
                             'price_unit': rec.unit_price,
                             'price_subtotal': rec.subtotal
                         })))
        for rec in search.lunch_ids:
            vals.append((Command.create(
                         {
                             'name': rec.item_id.name,
                             'quantity': rec.quantity,
                             'price_unit': rec.unit_price,
                             'price_subtotal': rec.subtotal
                         })))
        for rec in search.dinner_ids:
            vals.append((Command.create(
                         {
                             'name': rec.item_id.name,
                             'quantity': rec.quantity,
                             'price_unit': rec.unit_price,
                             'price_subtotal': rec.subtotal
                         })))
        for rec in search.snacks_ids:
            vals.append((Command.create(
                         {
                             'name': rec.item_id.name,
                             'quantity': rec.quantity,
                             'price_unit': rec.unit_price,
                             'price_subtotal': rec.subtotal
                         })))
        for rec in search.beverages_ids:
            vals.append((Command.create(
                         {
                             'name': rec.item_id.name,
                             'quantity': rec.quantity,
                             'price_unit': rec.unit_price,
                             'price_subtotal': rec.subtotal
                         })))

        invoice = self.env['account.move'].create([{
            'move_type': 'out_invoice',
            'partner_id': self.customer_id.id,
            'invoice_line_ids': vals,
            'invoice_origin': self.catering_id.name
        }])
        invoice.action_post()
        self.invoice_id = invoice.id
        return {
            'name': 'invoice',
            'view_mode': 'form',
            'res_id': invoice.id,
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
        }

    def invoice_button(self):
        """smart button - used to display created invoices"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('invoice_origin', '=', self.catering_id.name)],
            'context': "{'create':False}"
        }

    @api.depends("invoice_id.payment_state")
    def _compute_ribbon(self):
        """If payment state is paid then display paid ribbon on event booking"""
        for rec in self:
            print(self.invoice_id)
            if rec.invoice_id.payment_state == 'paid':
                rec.ribbon = True
            else:
                rec.ribbon = False


