class SheetsManager:
    def __init__(self, sheet):
        self.sheet = sheet
        self.spreadsheets = sheet.service.spreadsheets()

    def read_data_from_range(self, spreadsheet_id, sheet_range):
        return self.sheet.read_data_from_range(self.spreadsheets, spreadsheet_id, sheet_range)

    def write_data(self, spreadsheet_id, sheet_name, data):
        self.sheet.write_data(spreadsheet_id, sheet_name, data)

    def read_data_as_df(self, spreadsheet_id, sheet_name):
        return self.sheet.read_data_as_df(spreadsheet_id, sheet_name)

    def append_data(self, spreadsheet_id, sheet_name, data_df):
        self.sheet.append_data(spreadsheet_id, sheet_name, data_df)

    def write_to_range(self, data, spreadsheet_id, range_):
        self.__confirm_sheet_exist(spreadsheet_id, range_.split('!')[0])
        existing_data = self.read_data_from_range(spreadsheet_id, range_)
        if not existing_data:
            response = self.sheet.write_data_to_range(data, range_)
            print(response)
        else:
            response = self.sheet.append_data_to_range(data, range_)
        print(response)

    def sheet_exists(self, spreadsheet_id, sheet_name):
        # testing remove after
        return self.__confirm_sheet_exist(spreadsheet_id, sheet_name)


    @staticmethod
    def create_spreadsheet(title, scopes):
        import os
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        from googleapiclient.errors import HttpError
        if os.path.exists('../../private/token_personal.json'):
            creds = Credentials.from_authorized_user_file('../../private/token_personal.json', scopes)
        # creds, _ = google.auth.default()
        # pylint: disable=maybe-no-member
        try:
            service = build('sheets', 'v4', credentials=creds)
            spreadsheet = {'properties': {'title': title}}
            spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
            print(f"Spreadsheet ID: {(spreadsheet.get('spreadsheetId'))}")
            return spreadsheet.get('spreadsheetId')
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

    def __confirm_or_create(self, spreadsheet_id, sheet_name):
        sheet_exists = self.__confirm_sheet_exist(spreadsheet_id, sheet_name)
        return True if sheet_exists else self.__new_sheet(spreadsheet_id, sheet_name)

    def __confirm_sheet_exist(self, spreadsheet_id, sheet_name):
        spreadsheet = self.spreadsheets.get(spreadsheetId=spreadsheet_id).execute()
        sheets = spreadsheet.get('sheets', '')
        sheet_map = {s.get("properties", {}).get("title", ""): s for s in sheets}
        return sheet_name in sheet_map

    def __new_sheet(self, spreadsheet_id, sheet_name):
        requests = [{
            'addSheet': {
                'properties': {
                    'title': sheet_name
                }
            }
        }]
        body = {'requests': requests}
        self.spreadsheets.batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
