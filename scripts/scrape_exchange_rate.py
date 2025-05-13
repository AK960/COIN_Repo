from alpha_vantage.foreignexchange import ForeignExchange
import pandas as pd
import configparser

config = configparser.ConfigParser()
config.read('conf/config.ini')

# Access values from the configuration file
api_key = config.get('Alpha_Vantage_API', 'api_key')

# Set up Alpha Vantage ForeignExchange client
fx = ForeignExchange(key=api_key)

# Define the date range (adjust as needed)
from_date = '2023-05-01'
to_date = '2025-05-01'

# Fetch the exchange rate data for EUR to USD within the specified timeframe
data, meta_data = fx.get_currency_exchange_monthly(from_symbol='USD', to_symbol='EUR')

# Convert the data into a pandas DataFrame
df = pd.DataFrame(data).T  # Transpose so the date is the index
df.index = pd.to_datetime(df.index)  # Convert index to datetime

# Filter the data to the specific date range
df_filtered = df[(df.index >= from_date) & (df.index <= to_date)]

# Print the filtered data
print(df_filtered)

df_filtered.to_csv("usd_eur_230501-250501.csv")