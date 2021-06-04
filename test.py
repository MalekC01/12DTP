import requests 

api_url = "https://dev-api.shrimpy.io/v1/historical/candles"


data = requests.get(api_url).json()
print(data)


