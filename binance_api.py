import config
from binance.client import Client

api_key = "2A3InFFWjbLF8zElm9vTb0BTAMynIYuU6TKZjEAGQ7cN526xQNz5AgX71GnnHCvI"
secret_key = "h9epExjPvwPb4YZtTLDB74m5DGKHowQmHskC4l1RVXDZx36zdW3tdGoLekIXLavZ"

client = Client(config.api_key, config.api_secret)

prices = client.get_all_tickers()
print(prices)


