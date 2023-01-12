import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os


class Sheet:
    def __init__(self):
        # Set up authentication credentials
        scope = ['https://www.googleapis.com/auth/spreadsheets']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
                                                                       scope)

        # Open a connection to the Google Sheets API
        self.client = gspread.authorize(credentials)

    def read_data(self, spreadsheet_name, sheet_name):
        # Access the desired spreadsheet
        spreadsheet = self.client.open(spreadsheet_name)

        # Access the desired sheet in the spreadsheet
        worksheet = spreadsheet.worksheet(sheet_name)

        # Read data from the sheet
        data = worksheet.get_all_values()

        # Return the data
        return data

    def write_data(self, spreadsheet_name, sheet_name, data):
        # Access the desired spreadsheet
        spreadsheet = self.client.open(spreadsheet_name)

        # Access the desired sheet in the spreadsheet
        worksheet = spreadsheet.worksheet(sheet_name)

        # Write data to the sheet
        worksheet.append_rows(data)
