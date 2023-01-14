import pandas as pd
# from gspread_dataframe import set_with_dataframe
# from gspread_dataframe import get_as_dataframe


class SheetManipulator:
    def __init__(self, sheet_manager):
        self.sheet_manager = sheet_manager

    # def get_sheets_list(self, spreadsheet_id):
    #     result = self.sheet_manager.sheet.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    #     sheets = result.get('sheets', [])
    #     return sheets

    def insert_pivot_table(self, spreadsheet_name, sheet_name, data_range, new_sheet=False, pivot_sheet_name=None):
        spreadsheet = self.sheet_manager.sheet.service.open(spreadsheet_name)
        if new_sheet:
            pivot_sheet = spreadsheet.add_worksheet(title=pivot_sheet_name, rows=1, cols=1)
        else:
            pivot_sheet = spreadsheet.worksheet(pivot_sheet_name)
        pivot_sheet.insert_pivot_table(data_range)

    def change_data_range_format(self, spreadsheet_name, sheet_name, data_range, critical_points):
        worksheet = self.sheet_manager.sheet.service.open(spreadsheet_name).worksheet(sheet_name)
        data_range_values = worksheet.range(data_range)
        for cell in data_range_values:
            if cell.value in critical_points:
                cell.color = (1, 0.9, 0.9)  # set the color to light red
        worksheet.update_cells(data_range_values)

    def create_dashboard(self, spreadsheet_name, sheet_name, data_range):
        worksheet = self.sheet_manager.sheet.service.open(spreadsheet_name).worksheet(sheet_name)
        chart = worksheet.new_chart('BarChart')
        chart.add_series({'values': data_range})
        chart.set_title('Data Range Chart')
        chart.set_x_axis({'name': 'X-axis'})
        chart.set_y_axis({'name': 'Y-axis'})
        worksheet.insert_chart(chart)
