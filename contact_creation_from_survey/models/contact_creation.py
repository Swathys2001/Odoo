# -*- coding: utf-8 -*-
from odoo import fields, models


class ContactCreation(models.Model):
    """create a new model contact relation"""
    _name = 'contact.relation'

    survey_id = fields.Many2one('survey.survey', string="Survey id")
    question_id = fields.Many2one('survey.question',
                                  string="Questions",
                                  help="questions")
    contact_fields_id = fields.Many2one('ir.model.fields',
                                        string="Contact fields",
                                        help="contact fields",
                                        domain=[('model', '=', 'res.partner')])

