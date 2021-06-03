import requests 

api_url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/ohlc/range?vs_currency=usd&from=1392577232&to=1392577232"

data = requests.get(api_url).json()
print(data)