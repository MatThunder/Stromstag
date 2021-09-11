from entsoe import EntsoePandasClient
import sqlite3
import pandas as pd
from datetime import date, timedelta
import time


end_date = date.today()+timedelta(days=1)
current_date = end_date.strftime("%Y%m%d")

client = EntsoePandasClient(api_key='444fc771-5d0f-499f-9328-90c05c459219')

start = pd.Timestamp('20201109', tz='Europe/Brussels')
end = pd.Timestamp(current_date, tz='Europe/Brussels')
country_code = 'DE'


generation1 = client.query_load(country_code, start=start, end=end)

generation1.to_csv('outfile1.csv')
print(generation1)

start = pd.Timestamp('20201109', tz='Europe/Brussels')
end_date = date.today()+timedelta(days=2)
current_date = end_date.strftime("%Y%m%d")
end = pd.Timestamp(current_date, tz='Europe/Brussels')
country_code = 'DE'

generation2 = client.query_load_forecast(country_code, start=start, end=end)
generation2.to_csv('outfile2.csv')
print(generation2)
