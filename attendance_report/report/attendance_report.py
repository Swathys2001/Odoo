# -*- coding: utf-8 -*-
from odoo import api, models


class AttendanceReportDetails(models.AbstractModel):
    """abstract model for attendance report"""
    _name = 'attendance.reporting'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['attendance_report'].browse(docids)
        return {
                'doc_ids': docids,
                'doc_model': 'attendance.report',
                'docs': docs,
                'data': data,
            }