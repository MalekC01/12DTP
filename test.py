import requests 

key = "2129cf44-2bf1-4e11-968c-4d22f1580a40"
token =  "sk_bf573df0da8b4565b36735dda78f1755"
api_key = "31476228a2403339dab301fed858020ee23fb9967861fe558f551328e667a3cb"

#api_url = f"https://data.messari.io/api/v1/assets/btc/metrics/time-series?start=2020-01-01&end=2020-01-02&interval=1d"
#api_url = f"https://data.messari.io/api/v1/assets/btc/metrics/market-data/time-series?start=2020-01-01&end=2020-02-01&interval=1d"
#api_url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical"

api_url = f"https://api.coingecko.com/api/v3/coins/bitcoin/ohlc?vs_currency=usd&days=1&range?vs_currency=usd&from=1620172800&to=1620259200"

data = requests.get(api_url).json()
print(data)