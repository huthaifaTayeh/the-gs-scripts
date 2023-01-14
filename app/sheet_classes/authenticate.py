from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import os


class Authenticate:
    def __init__(self, scopes):
        self.scopes = scopes
        self.__creds = None

    def authenticate_with_creds(self, cred_json_filename):
        creds = None
        if os.path.exists('private/token.json'):
            creds = Credentials.from_authorized_user_file('private/token.json', self.scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            creds = self.__get_or_validate_creds(creds, cred_json_filename)
        self.__creds = creds

    def build_service(self):
        from googleapiclient.discovery import build
        return build('sheets', 'v4', credentials=self.__creds)

    def __get_or_validate_creds(self, creds, cred_json_filename):
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                cred_json_filename, self.scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('private/token.json', 'w') as token:
            token.write(creds.to_json())
        return creds
