import requests 
import datetime

token =  "sk_6d3688ec98d6451bb686b8ac277dce59"


#Tests stock to make sure it is a valid stock in the api
def stock_is_valid(stock):
  try:
    #test_stock =  f"https://cloud.iexapis.com/stable/stock/{stock}/company?&token={token}"
    test_stock = '{"symbol":"AAPL","companyName":"Apple Inc","exchange":"NASDAQ","industry":"Electronic Computer Manufacturing ","website":"https://www.apple.com/","description":"Apple Inc. is an American multinational technology company headquartered in Cupertino, California, that designs, develops, and sells consumer electronics, computer software, and online services. It is considered one of the Big Five companies in the U.S. information technology industry, along with Amazon, Google, Microsoft, and Facebook. Its hardware products include the iPhone smartphone, the iPad tablet computer, the Mac personal computer, the iPod portable media player, the Apple Watch smartwatch, the Apple TV digital media player, the AirPods wireless earbuds, the AirPods Max headphones, and the HomePod smart speaker line. Apples software includes iOS, iPadOS, macOS, watchOS, and tvOS operating systems, the iTunes media player, the Safari web browser, the Shazam music identifier, and the iLife and iWork creativity and productivity suites, as well as professional applications like Final Cut Pro X, Logic Pro, and Xcode. Its online services include the iTunes Store, the iOS App Store, Mac App Store, Apple Arcade, Apple Music, Apple TV+, iMessage, and iCloud. Other services include Apple Store, Genius Bar, AppleCare, Apple Pay, Apple Pay Cash, and Apple Card. Apple was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in April 1976 to develop and sell Wozniaks Apple I personal computer, though Wayne sold his share back within 12 days. It was incorporated as Apple Computer, Inc., in January 1977, and sales of its computers, including the Apple I and Apple II, grew quickly.","CEO":"Timothy Cook","securityName":"Apple Inc","issueType":"cs","sector":"Manufacturing","primarySicCode":3571,"employees":147000,"tags":["Electronic Technology","Telecommunications Equipment","Manufacturing","Electronic Computer Manufacturing "],"address":"1 Apple Park Way","address2":null,"state":"California","city":"Cupertino","zip":"95014-0642","country":"United States","phone":"14089961010"}'
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

  api_url =  '{"symbol":"AAPL","companyName":"Apple Inc","exchange":"NASDAQ","industry":"Electronic Computer Manufacturing ","website":"https://www.apple.com/","description":"Apple Inc. is an American multinational technology company headquartered in Cupertino, California, that designs, develops, and sells consumer electronics, computer software, and online services. It is considered one of the Big Five companies in the U.S. information technology industry, along with Amazon, Google, Microsoft, and Facebook. Its hardware products include the iPhone smartphone, the iPad tablet computer, the Mac personal computer, the iPod portable media player, the Apple Watch smartwatch, the Apple TV digital media player, the AirPods wireless earbuds, the AirPods Max headphones, and the HomePod smart speaker line. Apples software includes iOS, iPadOS, macOS, watchOS, and tvOS operating systems, the iTunes media player, the Safari web browser, the Shazam music identifier, and the iLife and iWork creativity and productivity suites, as well as professional applications like Final Cut Pro X, Logic Pro, and Xcode. Its online services include the iTunes Store, the iOS App Store, Mac App Store, Apple Arcade, Apple Music, Apple TV+, iMessage, and iCloud. Other services include Apple Store, Genius Bar, AppleCare, Apple Pay, Apple Pay Cash, and Apple Card. Apple was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in April 1976 to develop and sell Wozniaks Apple I personal computer, though Wayne sold his share back within 12 days. It was incorporated as Apple Computer, Inc., in January 1977, and sales of its computers, including the Apple I and Apple II, grew quickly.","CEO":"Timothy Cook","securityName":"Apple Inc","issueType":"cs","sector":"Manufacturing","primarySicCode":3571,"employees":147000,"tags":["Electronic Technology","Telecommunications Equipment","Manufacturing","Electronic Computer Manufacturing "],"address":"1 Apple Park Way","address2":null,"state":"California","city":"Cupertino","zip":"95014-0642","country":"United States","phone":"14089961010"}'

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

