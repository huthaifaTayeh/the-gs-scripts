import os
from dotenv import load_dotenv
from app.app import SheetsApp
from app.sheet_classes.sheet import Sheet
from app.sheet_classes.sheet_generator import SheetGenerator
from app.sheet_classes.sheet_manipulator import SheetManipulator
from app.sheet_classes.sheets_manager import SheetsManager
from app.sheet_classes.authenticate import Authenticate
from datetime import datetime, timedelta


def instantiate(scopes):
    auth = Authenticate(scopes)
    auth.authenticate_with_creds(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
    sheet_inst = Sheet(auth.build_service())
    sheets_mang_inst = SheetsManager(sheet_inst)
    sheet_gen_inst = SheetGenerator(sheet_inst, sheets_mang_inst)
    sheet_manip_inst = SheetManipulator(sheets_mang_inst)
    spreadsheet_id = os.environ.get("GOOGLE_SHEETS_SPREADSHEET_ID")
    app_inst = SheetsApp(scopes, spreadsheet_id, sheet_inst, sheets_mang_inst, sheet_gen_inst, sheet_manip_inst)
    return app_inst


# def add_data(app):
#     data = [
#         {
#             'marketer': 'Zaid',
#             'Campaigns': 'test'
#         }
#     ]
#     app.write_to_range(data, 'Sheet2!A:B')


def main():
    load_dotenv('./.env')
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    application = instantiate(scopes)
    current_year = int(datetime.now().year)
    application.hydrate_campaign_sheets()
    # application.prepare_campaign_sheets(campaign_weeks_formatter(current_year)) #formatter must do TODO format the sheets with conditional formats also
    # application.establish_connection(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
    # application.set_spreadsheet_id(os.environ.get("GOOGLE_SHEETS_SPREADSHEET_ID"))
    # marketers_list = application.marketers['marketer_name'].values.ravel()
    # print(marketers_list)
    # filter_column_name = 'marketer_team_id'
    # filter_value = '1'
    # mask = application.marketers[filter_column_name] == filter_value
    # print(mask)
    # filtered_column_list = marketers_list[mask]
    # print(filtered_column_list)
    # print(application.grouped_df_dict('teams'))


if __name__ == '__main__':
    main()
# app.new_spreadsheet("leila today's sheet")
# data = app.sheet.service.spreadsheets().values().get(spreadsheetId='1-e4JdsA23K-j7bAU_6kwC7zSXv3PaLAqi1NKY-xqNr0', range='Campaigns').execute()

# TODO implement Campaigns sheets for media and search auto generation if they don't exist
# TODO implement a google sheets chart plotter using python on Dashboard sheet ( check if sheet exists first)
# TODO use the chart plotter functionality to plot charts for Campaigns sheets ( ask leila for more functionalities )