# -*- coding: utf-8 -*-
from odoo.addons.survey.controllers.main import Survey
from odoo.http import request


class ContactCreation(Survey):
    """Inherit the controller survey"""
    def survey_submit(self, survey_token, answer_token, **post):
        """supering this function and add a new feature to create a contact"""
        survey = super().survey_submit(survey_token, answer_token, **post)
        access_data = self._get_access_data(survey_token, answer_token,
                                            ensure_token=True)
        survey_values = access_data['answer_sudo']
        user_values = survey_values['user_input_line_ids']
        contact_relation_ids = request.env['contact.relation'].search([])
        result = {}
        for val in user_values:
            for relation in contact_relation_ids:
                if val['question_id'] == relation.question_id:
                    result[relation.contact_fields_id.name] = val['value_char_box']
        if survey_values['state'] == 'done':
            request.env['res.partner'].sudo().create(result)
        return survey
