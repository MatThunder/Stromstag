from entsoe import EntsoePandasClient
import sqlite3
import pandas as pd
from datetime import date, timedelta


def time_difference_checking(df):
        df['Timedelta'] = df['Date'] - df['Date'].shift(-1)
        df.iloc[-1, df.columns.get_loc('Timedelta')] = pd.to_timedelta('-1 days +23:45:00')
        df.loc[df['Timedelta'] < '-1 days +23:45:00', 'equal_or_lower_than_15?'] = True
        df.loc[df['Timedelta'] >= '-1 days +23:45:00', 'equal_or_lower_than_15?'] = False
        df_r = df.reset_index(drop=True)
        df_r.insert(0, 'id', range(0, len(df)))
        return df_r

def datetime_format_change(data_frame):
        df2 = pd.DataFrame(columns=['Date_start', 'Date_end'])
        df2['Date_start'] = pd.to_datetime(data_frame['Date_start'])
        df2['Date_end'] = pd.to_datetime(data_frame['Date_end'])
        df2.insert(0, 'id', range(0, len(df2)))
        return df2

def time_periods_checking(data_frame_values, dataframe_check):
    if not dataframe_check.empty:
        # creating list of dataframes with time periods
        idx = data_frame_values.index[data_frame_values['equal_or_lower_than_15?']].values
        subset = data_frame_values.loc[0:idx[0], :]
        new_dfs_list = []
        for i in range(len(idx) - 1):
            subset2 = data_frame_values.loc[idx[i] + 1:idx[i + 1], :]
            new_dfs_list.append(subset2)
        subset_last = data_frame_values.loc[idx[-1] + 1:, :]

        # creating dataframe with the start and the end of time period
        df_new = pd.DataFrame(columns=['Date_start', 'Date_end'])
        df_new.loc[0, 'Date_start'] = subset.loc[0, 'Date']
        df_new.loc[0, 'Date_end'] = subset.loc[len(subset) - 1, 'Date']
        for i in range(len(idx) - 1):
            df_new.loc[i, 'Date_start'] = new_dfs_list[i].loc[idx[i] + 1, 'Date']
            df_new.loc[i, 'Date_end'] = new_dfs_list[i].loc[idx[i + 1], 'Date']
        df_new.loc[len(idx), 'Date_start'] = subset_last.loc[idx[len(idx) - 1] + 1, 'Date']
        df_new.loc[len(idx), 'Date_end'] = subset_last.loc[idx[len(idx) - 1] + len(subset_last) - 1, 'Date']

        dataframe=datetime_format_change(df_new)

    # if there is only one:
    else:
        df_new = pd.DataFrame(columns=['Date_start', 'Date_end'])
        df_new.loc[0, 'Date_start'] = data_frame_values.loc[0, 'Date']
        df_new.loc[0, 'Date_end'] = data_frame_values.loc[len(data_frame_values) - 1, 'Date']

        dataframe=datetime_format_change(df_new)

    return dataframe

def data_base_connection(table_name, dataframe):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    dataframe.to_sql(table_name, conn, if_exists='replace', index=False)
    sql = "SELECT * FROM " + table_name + ";"
    c.execute(sql)
    print("Database data:")
    for row in c.fetchall():
        print(row)
    #print(c.fetchall())


#ENTSOE API connecntion
client = EntsoePandasClient(api_key='444fc771-5d0f-499f-9328-90c05c459219')


#start and end date format
start_date_raw = date.today()
start_date = start_date_raw.strftime("%Y%m%d")

end_date_raw = date.today()+timedelta(days=1)
end_date = end_date_raw.strftime("%Y%m%d")

#quering load and renewable generation forecasts
start = pd.Timestamp(start_date, tz='Europe/Brussels')
end = pd.Timestamp(end_date, tz='Europe/Brussels')
country_code = 'DE'
load_raw = client.query_load_forecast(country_code, start=start, end=end)
renewable = client.query_wind_and_solar_forecast(country_code, start=start, end=end)

#formating load_raw to pandas dataframe
load = pd.DataFrame(load_raw)

#Algorithm
renewable['Total'] = renewable['Solar']+renewable['Wind Offshore']+renewable['Wind Onshore']
renewable['Renewable/Load_ratio'] = renewable['Total']/load[0]*100
renewable['Quality_ratio'] = renewable['Renewable/Load_ratio']/renewable['Renewable/Load_ratio'].max()*100

#Fomrating data: date, rounding values, etc...
renewable['Date'] = renewable.index
renewable.insert(0, 'id', range(0 , len(renewable)))
rounded_renewables = renewable['Quality_ratio'].round(decimals=1)
renewable['Quality_ratio'] = rounded_renewables
rounded_renewables = renewable['Renewable/Load_ratio'].round(decimals=1)
renewable['Renewable/Load_ratio'] = rounded_renewables

renewable.rename(columns={"Wind Offshore": "Wind_Offshore",
                                "Wind Onshore": "Wind_Onshore", "Renewable/Load_ratio": "Renewable_Load_ratio"}, inplace=True)


data_base_connection('Stromzeiten_app_stromzeiten_table', renewable)


#Looking for a time spans with Quality_ratio < 50
renewable.loc[renewable['Quality_ratio'] <50, 'equal_or_lower_than_50?'] = True
df = renewable[['Quality_ratio', 'equal_or_lower_than_50?', 'Date']]
df = df[df['equal_or_lower_than_50?'] == True]
df_r=time_difference_checking(df)
df2 = df_r[df_r['equal_or_lower_than_15?'] == True]
dataframe_bad_times = time_periods_checking(df_r,df2)
data_base_connection('Stromzeiten_app_schlechte_table', dataframe_bad_times)

#Looking for a time spans with Quality_ratio > 80
renewable.loc[renewable['Quality_ratio'] >80, 'equal_or_greater_than_80?'] = True
df = renewable[['Quality_ratio', 'equal_or_greater_than_80?', 'Date']]
df = df[df['equal_or_greater_than_80?'] == True]
df_r=time_difference_checking(df)
df2 = df_r[df_r['equal_or_lower_than_15?'] == True]
dataframe_best_times = time_periods_checking(df_r,df2)
data_base_connection('Stromzeiten_app_beste_table', dataframe_best_times)

#Looking for a time spans with Quality_ratio between 50 and 80
renewable.loc[renewable['Quality_ratio'].between(50, 80, inclusive=True), 'between_50_and_80?'] = True
df = renewable[['Quality_ratio', 'between_50_and_80?', 'Date']]
df.reset_index(drop=True)
df=df[df['between_50_and_80?'] == True]
df_r=time_difference_checking(df)
df2 = df_r[df_r['equal_or_lower_than_15?'] == True]
dataframe_good_times = time_periods_checking(df_r,df2)
data_base_connection('Stromzeiten_app_gute_table', dataframe_good_times)






