import datetime
from sheets_manager import SheetsManager
class SheetGenerator:
    def generate_weeks_dates(self, year):
        first_day_of_year = datetime.date(year, 1, 1)
        last_day_of_year = datetime.date(year, 12, 31)
        weeks = []
        for week in range(first_day_of_year.isocalendar()[1], last_day_of_year.isocalendar()[1] + 1):
            start_date = datetime.date.fromisocalendar(year, week, 1)
        end_date = datetime.date.fromisocalendar(year, week, 7)
        weeks.append((start_date, end_date))
        return weeks

    def generate_weeks_dates_column(self, spreadsheet_name, sheet_name, year):
        weeks = self.generate_weeks_dates(year)
        data = [[week[0].strftime("%Y-%m-%d"), week[1].strftime("%Y-%m-%d")] for week in weeks]
        sheets_manager = SheetsManager()
        sheets_manager.write_data(spreadsheet_name, sheet_name, data)
