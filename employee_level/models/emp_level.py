# -*- coding: utf-8 -*-
from odoo import fields, models


class EmployeeLevel(models.Model):
    """used to create a model for promotion"""
    _name = 'employee.level'
    _rec_name = 'level'

    salary = fields.Integer(string="Salary", help="Employee salary")
    level = fields.Selection(selection=[('1', '1'), ('2', '2'), ('3', '3'),
                                        ('4', '4'), ('5', '5')], string="Level",
                             help="Employee level")
