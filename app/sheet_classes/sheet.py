import pandas as pd


class Sheet:

    def __init__(self, service):
        self.service = service

    def set_service(self, service):
        self.service = service

    def read_data(self, spreadsheet_id, sheet_name):
        result = self.service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=sheet_name).execute()
        return result.get('values', [])

    @staticmethod
    def read_data_from_range(spreadsheets, spreadsheet_id, sheet_range):
        result = spreadsheets.values().get(spreadsheetId=spreadsheet_id, range=sheet_range).execute()
        values = result.get('values', [])
        result = pd.DataFrame(values[1:], columns=values[0]) if values else False
        return result

    def append_data_to_range(self, data, spreadsheet_id, range_):
        header_row = list(data[0][0].keys())

        # Convert the list of lists of dictionaries to a 2D array
        values = [header_row] + [[row.get(key, '') for key in row] for sublist in data for row in sublist]

        # Build the request body
        body = {'range': range_, 'values': values, 'majorDimension': 'ROWS'}
        return self.service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_,
                                                           valueInputOption='RAW', insertDataOption='INSERT_ROWS',
                                                           body=body).execute()

    def append_data(self, spreadsheet_id, sheet_name, data_df):
        data = data_df.values.tolist()
        self.write_data(spreadsheet_id, sheet_name, data)

    def write_data_to_range(self, data, range_, spreadsheet_id, types=None):
        print(data)
        import itertools
        if isinstance(types, pd.DataFrame):
            types_list = list(types['type'].to_dict().values())
            header_row = list(data[0][0].keys())
            header_row.append('types')
            values = [[row.get(key, '') for key in row] for sublist in data for row in sublist]
            result = [header_row] + [i + [j] for i, j in itertools.product(values, types_list)]
        else:
            result = [list(data[0].keys())]
        body = {'range': range_, 'values': result, 'majorDimension': 'ROWS'}
        self.service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_, valueInputOption='RAW',
                                                    body=body).execute()

    def write_data(self, spreadsheet_id, sheet_name, data):
        body = {'range': sheet_name, 'values': data, }
        result = self.service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=sheet_name,
                                                             valueInputOption='RAW', body=body).execute()

    def merge_column_dup_cells(self, spreadsheet_id, range_):
        result = self.service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_).execute()
        values = result.get('values', [])

        # Create a dictionary to store the start and end rows of each value
        value_rows = {}

        # Iterate through the rows and columns
        for i, row in enumerate(values):
            for j, val in enumerate(row):
                if val in value_rows:
                    # If the value already exists, update the end row
                    value_rows[val][1] = i
                else:
                    # If the value doesn't exist, add it to the dictionary
                    value_rows[val] = [i, i]

        # Create a list to store the merge cells requests
        requests = []

        # Iterate through the value rows dictionary
        for value, rows in value_rows.items():
            # Only merge cells if the start and end rows are different
            if rows[0] != rows[1]:
                requests.append({'mergeCells': {
                    'range': {'sheetId': 0, 'startRowIndex': rows[0], 'endRowIndex': rows[1] + 1, 'startColumnIndex': j,
                              'endColumnIndex': j + 1}, 'mergeType': 'MERGE_ALL'}})

        # Execute the merge cells requests
        if requests:
            self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': requests}).execute()

    def format_headers(self, spreadsheet_id, range_):
        cell_format = {"backgroundColor": {"red": 0.8, "green": 0.8, "blue": 0.8},
                       "textFormat": {"bold": True, "fontSize": 12,
                                      "foregroundColor": {"red": 0.0, "green": 0.0, "blue": 0.0}}}
        row_height = {"pixelSize": 30}
        request_body = {"requests": [{"repeatCell": {
            "range": {"sheetId": '1679181370', "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 7,
                      "endColumnIndex": 59}, "cell": {
                "userEnteredFormat": {"backgroundColor": {"red": 0.0, "green": 0.0, "blue": 0.0},
                                      "horizontalAlignment": "CENTER",
                                      "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0},
                                                     "fontSize": 12,
                                                     "bold": 'true'}}},
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"}}, {
            "updateSheetProperties": {"properties": {"sheetId": '1679181370', "gridProperties": {"frozenRowCount": 1}},
                                      "fields": "gridProperties.frozenRowCount"}}]}
        self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id,
                                                body=request_body).execute()  # from oauth2client.service_account import ServiceAccountCredentials
# def __init__(self):
#     self.client = None
# Set up authentication credentials
# scope = ['https://www.googleapis.com/auth/spreadsheets']
# credentials = ServiceAccountCredentials.from_json_keyfile_name(os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
#                                                                scope)
# self.client = gspread.authorize(credentials)
