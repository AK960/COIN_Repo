import yfinance as yf

# Get Tesla stock price history
tsla = yf.download("TSLA", start="2023-05-01", end="2025-05-01")
print(tsla.head())
tsla.to_csv("tsla_stock_230501-250501.csv")
 

