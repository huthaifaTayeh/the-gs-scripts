import os
from dotenv import load_dotenv

from app import SheetsApp
from sheet import Sheet
from sheet_generator import SheetGenerator
from sheet_manipulator import SheetManipulator
from sheets_manager import SheetsManager

load_dotenv('./.env')
sheet = Sheet()
sheets_manager = SheetsManager()
sheet_generator = SheetGenerator()
sheet_manipulator = SheetManipulator(sheets_manager)


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
app = SheetsApp(SCOPES, sheet, sheets_manager, sheet_generator, sheet_manipulator)
app.establish_connection(os.environ.get("CRED_FILE"))

