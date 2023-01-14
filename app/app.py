class SheetsApp:
    def __init__(self, scopes, sheet, sheets_manager, sheet_generator, sheet_manipulator):
        self.spreadsheet_id = None
        self.sheet = sheet
        self.sheets_manager = sheets_manager
        self.sheet_manipulator = sheet_manipulator
        self.sheet_generator = sheet_generator
        self.scopes = scopes
        self.sheets_list = []
        self.marketers = []

    def set_spreadsheet_id(self, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id

    def set_marketers(self, marketers_list):
        self.marketers = marketers_list

    def new_spreadsheet(self, title):
        self.sheets_manager.create_spreadsheet(title, self.scopes)

    def spreadsheets_list(self):
        self.sheets_manager.get_spreadsheets_list()

    def list_all_sheets(self, spreadsheet_id):
        self.sheets_list = self.sheets_manager.get_sheets_list(spreadsheet_id)

    def read_from_range(self, sheet_range):
        return self.sheets_manager.read_data_from_range(self.spreadsheet_id, sheet_range)

    def write_to_range(self, data, range_):
        self.sheets_manager.write_to_range(data, self.spreadsheet_id, range_)

    def sheet_exists(self, sheet_name):
        # testing remove after
        return self.sheets_manager.sheet_exists(self.spreadsheet_id, sheet_name)


