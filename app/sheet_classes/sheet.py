# import gspread
# import os


class Sheet:

    def __init__(self, service):
        self.service = service

    def set_service(self, service):
        self.service = service

    def read_data(self, spreadsheet_id, sheet_name):
        result = self.service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=sheet_name).execute()
        return result.get('values', [])

    def read_data_from_range(self, spreadsheets, spreadsheet_id, sheet_range):
        import pandas as pd
        result = spreadsheets.values().get(spreadsheetId=spreadsheet_id, range=sheet_range).execute()
        values = result.get('values', [])
        return pd.DataFrame(values[1:], columns=values[0])

    def append_data_to_range(self, data, range_):
        values_to_append = []
        for row in data:
            row_values = []
            for header, value in row.items():
                row_values.append(value)
            values_to_append.append(row_values)
        request_body = {
            'values': values_to_append
        }
        return self.sheet.service.spreadsheets().values().append(spreadsheetId=self.spreadsheet_id,
                                                                 range=range_,
                                                                 valueInputOption='RAW',
                                                                 insertDataOption='INSERT_ROWS',
                                                                 body=request_body).execute()

    def append_data(self, spreadsheet_id, sheet_name, data_df):
        data = data_df.values.tolist()
        self.write_data(spreadsheet_id, sheet_name, data)

    def write_data_to_range(self, data, range_):
        values_to_write = []
        headers = []
        for row in data:
            row_values = []
            for header, value in row.items():
                row_values.append(value)
                headers.append(header)
            values_to_write.append(headers)
            values_to_write.append(row_values)
        request_body = {
            'range': range_,
            'values': values_to_write,
            'majorDimension': 'ROWS'
        }
        return self.sheet.service.spreadsheets().values().update(spreadsheetId=self.spreadsheet_id,
                                                                 range=range_, body=request_body,
                                                                 valueInputOption='RAW').execute()

    def write_data(self, spreadsheet_id, sheet_name, data):
        body = {
            'range': sheet_name,
            'values': data,
        }
        result = self.sheet.service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=sheet_name,
                                                                   valueInputOption='RAW', body=body).execute()
# from oauth2client.service_account import ServiceAccountCredentials
# def __init__(self):
#     self.client = None
# Set up authentication credentials
# scope = ['https://www.googleapis.com/auth/spreadsheets']
# credentials = ServiceAccountCredentials.from_json_keyfile_name(os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
#                                                                scope)
# self.client = gspread.authorize(credentials)
