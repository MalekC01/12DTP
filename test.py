import yfinance as yf
import pandas as pd

msft = yf.Ticker("MSsscsFT")

date = "2021-06-30"

data = msft.get_info()

print(data)

