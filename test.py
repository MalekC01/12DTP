import yfinance as yf
import pandas as pd

msft = yf.Ticker("MSFT")

hist = msft.history(period="max")

print(hist)

thing = hist['Close'].to_csv()

print(thing)