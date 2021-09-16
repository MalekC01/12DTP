import yfinance as yf

msft = yf.Ticker("MSFT")

desc =[]

data = msft.info

desc.append(data['longBusinessSummary'])
print(desc)
