import yfinance as yf
import pandas as pd

msft = yf.Ticker("MSFT")

date = "2021-06-30"

data = msft.history(start=date)

print(data)
print(data['Open'][1])

