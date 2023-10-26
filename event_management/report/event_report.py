from odoo import models,api


class EventFormReport(models.AbstractModel):

   _name = 'event.reporting'

   @api.model
   def _get_report_values(self, docids, data=None):
        docs = self.env['event_report'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'event.booking',
            'docs': docs,
            'data': data,
        }
