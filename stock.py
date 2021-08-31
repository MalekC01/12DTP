import requests 
import datetime

token =  "sk_65b776f2c4c242878b154ac942eaba27"


#Tests stock to make sure it is a valid stock in the api
def stock_is_valid(stock):
  try:
    test_stock =  f"https://cloud.iexapis.com/stable/stock/{stock}/company?&token={token}"
    requests.get(test_stock).json()
    return True
  except:
    print("\nThis stock doesnt exist try agian.\n")
    return False


def test(id):
  print(id + "hi")


#Makes sure that that the market was open on that day
def is_date_valid(date):

  info_of_date = ""

  if len(date) != 10:
    return False, 'Length of date is wrong (DD/MM/YYYY)'

  for i in range(len(date)):
    if i == 2 or i == 5:
      if date[i] != "/":
        return False, 'Make sure to add a / after the days and month. (DD/MM/YYYY'
    else:
      if not date[i].isdigit():
        return False, 'Date must be entered in intergers'

  date_list = date.split('/')

  year = date_list[2]
  month = date_list[1]
  day = date_list[0]


  if int(year) not in range(2016, 2022):
    return False, 'Year must be in the last 5 years (2016-2021).'

  if int(month) not in range(1, 13):
    return False, 'Month must be between 1-12'

  if int(day) not in range(1, 32):
    return False, 'Day must be between 1-31'
    
  is_day_a_weekday = datetime.datetime(int(year), int(month), int(day))
  day_name = is_day_a_weekday.strftime("%A")

  if day_name == "Saturday" or day_name == "Sunday":
    return False, 'Market is not open in the weekend.'

  info_of_date = year + month + day

  return True, info_of_date


data_date = []
date_high = []
date_low = []
date_open = []
date_close = []
decription_blurb = []

def clear_data():
  data_date = []
  date_high = []
  date_low = []
  date_open = []
  date_close = []


#takes the input from the stock name a date and gets the data from the api
def get_data(stock_name, date_string):

  api_url =  f"https://cloud.iexapis.com/stable/stock/{stock_name}/chart/date/{date_string}?&token={token}&chartByDay=true"
  print(api_url)

  data = requests.get(api_url).json()[0]
  
  data_date = []
  date_high = []
  date_low = []
  date_open = []
  date_close = []


  data_date.append(data['date'])
  date_high.append(data['high'])
  date_low.append(data['low'])
  date_open.append(data['open'])
  date_close.append(data['close'])

  raw_data = {"date": data_date[0],
              "high": date_high[0],
              "low": date_low[0],
              "open": date_open[0], 
              "close": date_close[0]}
  

  return raw_data

