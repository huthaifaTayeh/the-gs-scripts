from app import App
from sheet import Sheet
from sheet_generator import SheetGenerator
from sheet_manipulator import SheetManipulator
from sheets_manager import SheetsManager

sheet, sheets_manager, sheet_generator, sheet_manipulator = Sheet(), SheetsManager(), SheetGenerator, SheetManipulator(
    sheets_manager)

app = App(sheet, sheets_manager, sheet_generator, sheet_manipulator)
