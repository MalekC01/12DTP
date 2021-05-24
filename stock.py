import requests 

token =  "sk_bf573df0da8b4565b36735dda78f1755"

api_url = f"https://cloud.iexapis.com/stable/stock/aapl/quote/?token={token}"

data = requests.get(api_url).json()
print(data)