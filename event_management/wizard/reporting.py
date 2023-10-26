import io
from odoo import fields, models
from odoo.exceptions import ValidationError, MissingError
import xlsxwriter
from odoo.tools import date_utils
import json


class Reporting(models.TransientModel):
    """Used to write query and all validations done here"""
    _name = 'event.report'
    _description = "Report of the event management"

    from_date = fields.Date()
    to_date = fields.Date()
    event_type_ids = fields.Many2many("event.management", string="Event type")
    catering = fields.Boolean(default=False)
    current_date = fields.Date(default=fields.Datetime.today())

    def print_report(self):
        """This function used to print report"""
        if self.from_date and self.to_date:
            if self.from_date > self.to_date:
                raise ValidationError("Invalid dates")
        query = """select eb.name as event_name,em.name as type,
                   eb.booking_date,eb.state,ec.grand_total,eb.customer_id,
                   eb.event_start_date,eb.event_end_date,eb.booking_date,ec.id,
                   res.name as customer 
                   from event_management_booking as eb
                   inner join res_partner as res on res.id = eb.customer_id
                   inner join event_management as em on eb.event_type_id = em.id
                   inner join event_catering as ec on eb.id = ec.event_id"""
        date_from = False
        date_end = False
        event_name = False
        today_date = False
        if not date_from and not date_end:
            today_date = self.current_date
        if self.from_date:
            date_from = self.from_date
            query += f"""
            and eb.booking_date >= '{self.from_date}'"""
        if self.to_date:
            date_end = self.to_date
            query += f"""
            and eb.booking_date <= '{self.to_date}'"""
        if self.event_type_ids:
            event = tuple(i.id for i in self.event_type_ids)
            print(event)
            if len(event) > 1:
                query += f"""
                      and eb.event_type_id in {event}"""
            else:
                query += f"""
                      and eb.event_type_id = {self.event_type_ids.id}"""
            event_name = tuple(i.name for i in self.event_type_ids)
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        data = {'date_from': date_from,
                'date_end': date_end,
                'today_date': today_date,
                'event': event_name,
                'caterings': False,
                'report': report}
        if self.catering:
            for i in report:
                catering_query = f"""
                select ec.id, cf.item_id,cf.quantity,cf.unit_price, cm.name as food, 
                eb.name,cf.subtotal,uom.name as uom from event_catering as ec
                inner join catering_food as cf on ec.id = cf.lunch_id or
                ec.id = cf.dinner_id or ec.id = cf.break_fast_id or 
                ec.id = cf.snacks_id or ec.id = cf.welcome_drink_id or
                ec.id = cf.beverage_id
                inner join catering_menu as cm on cf.item_id = cm.id
                inner join event_management_booking as eb on ec.event_id = eb.id
                inner join uom_uom as uom on cf.uom = uom.id 
                where ec.id = {i['id']}"""
                self.env.cr.execute(catering_query)
                catering_menu = self.env.cr.dictfetchall()
                i['catering'] = catering_menu
                print(catering_menu)
            data['caterings'] = True
        print(data)
        print("report",report)
        if not report:
            raise MissingError("No records found")
        return self.env.ref(
            'event_management.action_event_booking_form').report_action(
            None, data=data)

    def print_xlsx(self):
        """XLSX button action"""
        if self.from_date and self.to_date:
            if self.from_date > self.to_date:
                raise ValidationError("Invalid dates")
        query = """select eb.name as event_name,em.name as type,
                          eb.booking_date,eb.state,ec.grand_total,eb.customer_id,
                          eb.event_start_date,eb.event_end_date,eb.booking_date,ec.id,
                          res.name as customer 
                          from event_management_booking as eb
                          inner join res_partner as res on res.id = eb.customer_id
                          inner join event_management as em on eb.event_type_id = em.id
                          inner join event_catering as ec on eb.id = ec.event_id"""
        date_from = False
        date_end = False
        event_name = False
        today_date = False
        if not date_from and not date_end:
            today_date = self.current_date
        if self.from_date:
            date_from = self.from_date
            query += f"""
                   and eb.booking_date >= '{self.from_date}'"""
        if self.to_date:
            date_end = self.to_date
            query += f"""
                   and eb.booking_date <= '{self.to_date}'"""
        if self.event_type_ids:
            event = tuple(i.id for i in self.event_type_ids)
            if len(event) > 1:
                query += f"""
                             and eb.event_type_id in {event}"""
            else:
                query += f"""
                             and eb.event_type_id = {self.event_type_ids.id}"""
            event_name = tuple(i.name for i in self.event_type_ids)
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        data = {'date_from': date_from,
                'date_end': date_end,
                'today_date': today_date,
                'event': event_name,
                'caterings': False,
                'report': report}
        if self.catering:
            for i in report:
                catering_query = f"""
                       select ec.id, cf.item_id,cf.quantity,cf.unit_price, 
                       cm.name as food,eb.name,cf.subtotal,uom.name as uom 
                       from event_catering as ec inner join catering_food as cf 
                       on ec.id = cf.lunch_id or ec.id = cf.dinner_id or
                       ec.id = cf.break_fast_id or ec.id = cf.snacks_id or 
                       ec.id = cf.welcome_drink_id or ec.id = cf.beverage_id
                       inner join catering_menu as cm on cf.item_id = cm.id
                       inner join event_management_booking as eb on 
                       ec.event_id = eb.id inner join uom_uom as uom on 
                       cf.uom = uom.id where ec.id = {i['id']}"""
                self.env.cr.execute(catering_query)
                catering_menu = self.env.cr.dictfetchall()
                i['catering'] = catering_menu
            data['caterings'] = True
        if not report:
            raise MissingError("No records found")
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'event.report',
                     'options': json.dumps(data, default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        """To show XLSX report"""
        from_date = data['date_from']
        to_date = data['date_end']
        event = data['event']
        report = data['report']
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        if event:
            col_num = 2
            row_num = 5
            sheet.merge_range('A6:B6', 'Event type:', cell_format)
            for i in event:
                sheet.merge_range(row_num,col_num,row_num,col_num+1, i, cell_format)
                col_num += 2
        sheet.merge_range('B2:I3', 'EXCEL REPORT', head)
        sheet.merge_range('A8:B8', 'From Date:', cell_format)
        sheet.merge_range('C8:D8', from_date, txt)
        sheet.write('F8', 'To Date:', cell_format)
        sheet.merge_range('G8:H8', to_date, txt)
        sheet.write('A10', 'Sl.no:', cell_format)
        sheet.merge_range('B10:E10', 'Event name', cell_format)
        col = 5
        row = 9
        if not event:
            sheet.merge_range(row, col, row, col+1, 'Event type', cell_format)
            col += 2
        sheet.merge_range(row, col, row, col+1, 'Customer name', cell_format)
        sheet.merge_range(row, col+2, row, col+3, 'Booking date', cell_format)
        sheet.merge_range(row, col+4, row, col+5, 'Status', cell_format)
        sheet.merge_range(row, col+6, row, col+7, 'Total', cell_format)
        if report:
            row_num = 11
            serial = 1
            sum_total = 0
            for record in report:
                col_num = 0
                sheet.write(row_num, col_num,
                            serial,txt)
                sheet.merge_range(row_num, col_num+1, row_num, col_num +4,
                                  record['event_name'],
                                  txt)
                col = col_num + 5
                if not event:
                    sheet.merge_range(row_num, col, row_num, col + 1,
                                      record['type'],
                                      txt)
                    col_num += 2
                sheet.merge_range(row_num, col_num+5, row_num, col_num + 6,
                                  record['customer'],
                                  txt)
                sheet.merge_range(row_num, col_num+7, row_num, col_num + 8,
                                  record['booking_date'],
                                  txt)
                sheet.merge_range(row_num, col_num+9, row_num, col_num + 10,
                                  record['state'],
                                  txt)
                sheet.merge_range(row_num, col_num+11, row_num, col_num+12,
                                  record['grand_total'],
                                  txt)
                row_num += 1
                serial += 1
                sum_total += record['grand_total']
            row = row_num + 1
            col = 9
            sheet.merge_range(row, col, row, col + 1,
                              'Total:',
                              txt)
            sheet.merge_range(row, col + 2, row, col + 3,
                              sum_total, txt)
            if data['caterings']:
                col = 1
                row = row_num + 3
                sheet.merge_range(row, col, row, col + 3, 'Catering details',
                                  cell_format)
                row += 2
                sheet.merge_range(row, col, row, col + 3, 'Event Name',
                                  cell_format)
                sheet.merge_range(row, col + 4, row, col + 5, 'Item', cell_format)
                sheet.merge_range(row, col + 6, row, col + 7, 'Qty', cell_format)
                sheet.merge_range(row, col + 8, row, col + 9, 'UOM', cell_format)
                sheet.merge_range(row, col + 10, row, col + 11, 'Unit price',
                                  cell_format)
                sheet.merge_range(row, col + 12, row, col + 13, 'Subtotal',
                                  cell_format)
                row_num = row + 1
                for rec in report:
                    for re in rec['catering']:
                        col_num = 0
                        sheet.merge_range(row_num, col_num, row_num, col_num + 4,
                                          re['name'],
                                          txt)
                        sheet.merge_range(row_num, col_num + 5, row_num,
                                          col_num + 6,
                                          re['food'],
                                          txt)
                        sheet.merge_range(row_num, col_num + 7, row_num,
                                          col_num + 8,
                                          re['quantity'],
                                          txt)
                        sheet.merge_range(row_num, col_num + 9, row_num,
                                          col_num + 10,
                                          re['uom']['en_US'],
                                          txt)
                        sheet.merge_range(row_num, col_num + 11, row_num,
                                          col_num + 12,
                                          re['unit_price'],
                                          txt)
                        sheet.merge_range(row_num, col_num + 13, row_num,
                                          col_num + 14,  re['subtotal'],
                                          txt)
                        row_num += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
