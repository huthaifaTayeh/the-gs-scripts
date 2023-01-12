from sheet import Sheet

class SheetsManager:
    def __init__(self):
        self.sheet = Sheet()

    def create_sheet(self, spreadsheet_name, sheet_name):
        spreadsheet = self.sheet.client.open(spreadsheet_name)
        spreadsheet.add_worksheet(title=sheet_name, rows=1, cols=1)

    def read_data(self, spreadsheet_name, sheet_name):
        return self.sheet.read_data(spreadsheet_name, sheet_name)

    def write_data(self, spreadsheet_name, sheet_name, data):
        self.sheet.write_data(spreadsheet_name, sheet_name, data)
