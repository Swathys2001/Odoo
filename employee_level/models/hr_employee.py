# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    """Inherit hr model and add two fields"""
    _inherit = 'hr.employee'

    level = fields.Many2one('employee.level', string="Level",
                            help="Employee level")
    salary = fields.Integer(related="level.salary", string="Salary",
                            help="Employee salary")
    last_level = fields.Boolean(default=False)

    def promotion_button(self):
        """button action - level and salary changes"""
        current_level = self.level.level
        last_level = self.env.ref('employee_level.fifth_level_record').id
        new_level = int(current_level) + 1
        new = self.env['employee.level'].search([('level', '=', new_level)])
        self.level = new
        if new_level >= last_level:
            self.last_level = True

