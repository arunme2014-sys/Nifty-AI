import yfinance as yf

ticker = yf.Ticker("^NSEI")

df = ticker.history(period="10y")

df.to_csv("data/nifty_daily.csv")

print(df.head())

print("Saved Successfully")