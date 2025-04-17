import yfinance as yf

# Get Tesla stock price history
tsla = yf.download("TSLA", start="2022-01-01", end="2025-01-01")
print(tsla.head())
tsla.to_csv("tsla_stock_220101-250101.csv")
 

