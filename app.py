import gspread
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os


class SheetsApp:
    def __init__(self, scopes, sheet, sheets_manager, sheet_generator, sheet_manipulator):
        self.sheet = sheet
        self.sheets_manager = sheets_manager
        self.sheet_manipulator = sheet_manipulator
        self.sheet_generator = sheet_generator
        self.scopes = scopes

    def establish_connection(self, cred_json_filename):
        # gspread_client = gspread.service_account(cred_json_filename)
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    cred_json_filename, self.scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
