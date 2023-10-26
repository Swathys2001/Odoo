# -*- coding: utf-8 -*-
from odoo import fields, models


class SurveySurvey(models.Model):
    """inherit model survey_survey"""
    _inherit = 'survey.survey'

    contact_ids = fields.One2many('contact.relation',
                                  'survey_id', string="Contacts",
                                  help="Add the details for creating a "
                                       "new contact")
