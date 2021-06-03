import requests 
import datetime

token =  "sk_bf573df0da8b4565b36735dda78f1755"

loop = True

while loop:
  print("Data is avalible from the last 5 years.\n")

  investment_type = True

  stock_exists = False
  stock = ''

  while not stock_exists:
    stock = input("Use the 4 letter ticker: ")
    try:
      test_stock =  f"https://cloud.iexapis.com/stable/stock/{stock}/company?&token={token}"
      requests.get(test_stock).json()
      stock_exists = True
    except:
      print("\nThis stock doesnt exist try agian.\n")

  info_of_date = ""
  year = ""
  month = ""
  day = ""

  day_is_a_weekday = False

  while not day_is_a_weekday:

    print("\nWhat date you would like to see data about?\nMust be in the last 5 years.\n")
    year_correct = False
    while not year_correct:
      year = int(input("Year: "))
      if year not in range(2016, 2022):
        print("Year must be within 2016-2021.")
      else:
          year_correct = True

    month_correct = False
    while not month_correct:
      month = int(input("Month: "))
      if month not in range(1, 13):
        print("Month must be between 1-12, for single digit months put a 0 infront.")
      else:
        month_correct = True
      if month in range(1, 10):
        month = "0" + str(month)

    day_correct = False
    while not day_correct:
      day = int(input("Day: "))
      if day not in range(1, 32):
        print("Day must be between 1-31, for single digit days put a 0 infront.")
      else:
        day_correct = True
      if day in range(1, 10):
        day = "0" + str(day)

    info_of_date = str(year) + str(month) + str(day)
    is_day_a_weekday = datetime.datetime(int(year), int(month), int(day))
    day_name = is_day_a_weekday.strftime("%A")

    if day_name == "Saturday" or day_name == "Sunday":
      print("\nThe stock market is only open Monday-Friday. Try again.")
    else:
      day_is_a_weekday = True

  api_url =  f"https://cloud.iexapis.com/stable/stock/{stock}/chart/date/{info_of_date}?&token={token}&chartByDay=true"

  data = requests.get(api_url).json()

  data_date = []
  date_high = []
  date_low = []
  date_open = []
  date_close = []

  for i in range(len(data)):
    data_date.append(data[i]['date'])
    date_high.append(data[i]['high'])
    date_low.append(data[i]['low'])
    date_open.append(data[i]['open'])
    date_close.append(data[i]['close'])
    
  if len(date_high) == 0:
    print("\nThe market was closed on " + str(year) + " " + str(month) + " " + str(day))
  else:
    print("\nAll prices are in $USD\n")
    print("Date: " + str(data_date[0]))
    print("High: $" + str(date_high[0]))
    print("Low: $" + str(date_low[0]))
    print("Open: $" + str(date_open[0]))
    print("Close: $" + str(date_close[0]))

  more_data = True

  while more_data:
    more_data = input("\nWould you like to see more data? Yes or No. ")

    if more_data == "no" or more_data == "No":
      more_data = False
      loop = False
    elif more_data == "yes" or more_data == "Yes":
      more_data = False
    else:
      print("Type Yes or No.")
