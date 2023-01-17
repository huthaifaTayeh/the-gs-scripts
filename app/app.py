from datetime import datetime, timedelta

import pandas as pd


class SheetsApp:
    def __init__(self, scopes, spreadsheet_id, sheet, sheets_manager, sheet_generator, sheet_manipulator):
        self.spreadsheet_id = spreadsheet_id
        self.sheet = sheet
        self.sheets_manager = sheets_manager
        self.sheet_manipulator = sheet_manipulator
        self.sheet_generator = sheet_generator
        self.scopes = scopes
        self.sheets_df = pd.DataFrame()
        self.marketers_df = pd.DataFrame()
        self.marketing_accounts_df = pd.DataFrame()
        self.marketing_teams_df = pd.DataFrame()
        self.marketing_services_df = pd.DataFrame()
        self.marketing_channels_df = pd.DataFrame()
        self.types = pd.DataFrame()
        self.set_meta_data_lists()

    def set_spreadsheet_id(self, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id

    def new_spreadsheet(self, title):
        self.sheets_manager.create_spreadsheet(title, self.scopes)

    def spreadsheets_list(self):
        self.sheets_manager.get_spreadsheets_list()

    def list_all_sheets(self, spreadsheet_id):
        self.sheets_df = self.sheets_manager.get_sheets_list(spreadsheet_id)

    def read_from_range(self, sheet_range):
        return self.sheets_manager.read_data_from_range(self.spreadsheet_id, sheet_range)

    def write_to_range(self, data, range_):
        self.sheets_manager.write_to_range(data, self.spreadsheet_id, range_)

    def sheet_exists(self, sheet_name):
        # testing remove after
        return self.sheets_manager.sheet_exists(self.spreadsheet_id, sheet_name)

    def set_meta_data_lists(self):
        if self.sheet_exists('meta-data'):
            self.__set_marketers(self.read_from_range('meta-data!A:C'))
            self.__set_marketing_teams(self.read_from_range('meta-data!K:L'))
            self.__set_marketing_accounts(self.read_from_range('meta-data!E:J'))
            self.__set_marketing_services(self.read_from_range('meta-data!N:O'))
            self.__set_marketing_channels(self.read_from_range('meta-data!Q:R'))
            self.types = self.__get_types()
            return True
        else:
            return False

    def hydrate_campaign_sheets(self):
        # if not self.sheets_manager.sheet_exists(spreadsheet_id=self.spreadsheet_id, sheet_name='media-campaign'):
        self.prepare_campaign_sheets(self.__format_weeks_headers())
        campaign_temp_dict = self.grouped_df_dict('teams')
        for team, team_data_list in campaign_temp_dict.items():
            self.sheets_manager.write_to_range(range_=f'{team}-campaign!A:F', data=team_data_list,
                                               spreadsheet_id=self.spreadsheet_id, types=self.types)
            # self.sheets_manager.merge_dup_cells(spreadsheet_id=self.spreadsheet_id, range_=f'{team}-campaign!A:F')
        print('should be done!')

    def prepare_campaign_sheets(self, weeks_formatted_list):
        weeks_formatted_dict = {}
        for week in weeks_formatted_list:
            weeks_formatted_dict[week] = ''
        for weeks_range in ['search-campaign!G:BF', 'media-campaign!G:BF']:
            self.sheets_manager.write_to_range(data=[weeks_formatted_dict], spreadsheet_id=self.spreadsheet_id,
                                               range_=weeks_range)
            self.sheets_manager.sheet.format_headers(spreadsheet_id=self.spreadsheet_id,
                                                     range_=weeks_range.replace('G', 'G1').replace('BF', 'BF1'))

    def grouped_df_dict(self, group_by):
        # output = {}
        grouped_dict = self.group_dfs_by(group_by)
        # grouper = self.__dict__['marketing_' + group_by + '_df']
        # dataframes = [self.marketers_df, self.marketing_accounts_df] if group_by == 'team' else [self.marketers_df,
        #                                                                                          self.marketing_services_df,
        #                                                                                          self.marketing_teams_df]
        # for team_id, group in grouped:
        #     group.dropna()
        #     team_name = grouper.loc[grouper['team_id'] == team_id, 'team_name'].iloc[0]
        #     output[team_name] = {}
        #     for df in dataframes:
        #         df_name = list(df.columns)[0].split('_')[0] + 's'  # Pluralize the dataframe name
        #         output[team_name][df_name] = group.loc[group['team_id'] == team_id, df.columns].to_dict('records')
        return grouped_dict

    def group_dfs_by(self, group_by):
        return self.solve_for(group_by)

    def solve_for(self, name: str):
        do = f"_SheetsApp__group_by_{name}"
        if hasattr(self, do) and callable(func := getattr(self, do)):
            print('YUUUUUp')
            return func()

    def __set_marketers(self, marketers_df):
        self.marketers_df = marketers_df

    def __set_marketing_teams(self, teams_df):
        self.marketing_teams_df = teams_df

    def __set_marketing_accounts(self, accounts_df):
        self.marketing_accounts_df = accounts_df

    def __set_marketing_channels(self, channels_df):
        self.marketing_channels_df = channels_df

    def __set_marketing_services(self, services_df):
        self.marketing_services_df = services_df

    def __get_df_column_list(self, attr_name, column_header):
        return self.__dict__[attr_name][column_header].values.ravel()

    def __group_by_teams(self):
        output = {}
        dataframes_list = []
        merged_df = self.marketing_teams_df.merge(self.marketers_df, on='team_id').merge(self.marketing_accounts_df,
                                                                                         on='marketer_id').merge(
            self.marketing_services_df, on='service_id').merge(self.marketing_channels_df, on='channel_id')
        grouped = merged_df.groupby('team_name')
        for team_name, group in grouped:
            output[team_name] = self.__create_nested_dict(group)
        # for item in ['marketers', 'marketing_accounts']:
        #     dataframes_list.append(self.__dict__[item + '_df'])
        # grouped_by_team = pd.concat(dataframes_list, axis=0).groupby('team_id')
        return output

    @staticmethod
    def __format_weeks_headers():
        weeks_list = []
        year = int(datetime.now().year)
        for i in range(1, 53):
            week_start = datetime.strptime(f'{year}-W{i}-1', '%Y-W%U-%w')
            week_end = week_start + timedelta(days=6)
            week_str = f'w23-{i}' + ' ' + week_start.strftime('%d-%m-%Y') + ' to ' + week_end.strftime('%d-%m-%Y')
            weeks_list.append(week_str)
        return weeks_list

    @staticmethod
    def __create_nested_dict(group: pd.DataFrame):
        # user_name = group['marketer_name'].tolist()
        accounts = group.groupby('marketer_name').apply(
            lambda x: x[['marketer_name', 'account_name', 'service_name', 'channel_name']].to_dict('records')).tolist()
        return accounts

    def __get_types(self):
        return self.sheets_manager.read_data_from_range(spreadsheet_id=self.spreadsheet_id,
                                                        sheet_range='meta-data!T1:T12')
