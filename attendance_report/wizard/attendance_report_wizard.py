from odoo import fields, models
from odoo.exceptions import MissingError


class AttendanceReport(models.TransientModel):
    """Transient model for wizard of report"""
    _name = 'attendance.report'

    date = fields.Datetime()
    absentees = fields.Boolean()

    def print_report(self):
        """This function used to print report"""
        query = """select hr.name as employee_id,at.check_in,check_out,
        at.worked_hours from hr_attendance as at inner join 
        hr_employee as hr on hr.id = at.employee_id"""
        report_date = False
        if self.date:
            report_date = self.date
            query += f""" where at.check_in <= '{self.date}' and at.check_out >= '{self.date}'"""
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        data = {
                'date': report_date,
                'absentees_details': False,
                'report': report}
        if self.absentees:
            for i in report:
                absentees_query = f"""select e.id as employee_id, e.name
                as employee_name from hr_employee e where not exists ( select *
                from hr_attendance a where a.employee_id = e.id 
                and a.check_in::date = '{self.date}') order by e.name"""
                self.env.cr.execute(absentees_query)
                absentees_details = self.env.cr.dictfetchall()
                i['absentees'] = absentees_details
            data['absentees_details'] = True
        if not report:
            raise MissingError("No records found")
        return self.env.ref(
            'attendance_report.action_attendance_report_form').report_action(
            None, data=data)
