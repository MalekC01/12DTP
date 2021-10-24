import requests
import datetime
import yfinance as yf


# Tests stock to make sure it is a valid stock in the api
def stock_is_valid(stock):
    ticker = yf.Ticker(stock)
    try:
        some_data = ticker.splits[0]
        return True
    except IndexError:
        return False


# Makes sure that that the market was open on that day
def is_date_valid(date):

    info_of_date = ""

    # checks formatting of the users input.
    if len(date) != 10:
        return False, 'Length of date is wrong (DD/MM/YYYY)'

    for i in range(len(date)):
        if i == 2 or i == 5:
            if date[i] != "/":
                return False, 'Make sure to add a / after the days and month. (DD/MM/YYYY)'
        else:
            if not date[i].isdigit():
                return False, 'Date must be entered in intergers'

    # formats users input into a form that can be understood by the API.
    date_list = date.split('/')

    year = date_list[2]
    month = date_list[1]
    day = date_list[0]

    # check
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

    info_of_date = year + '-' + month + '-' + day

    return True, info_of_date


# creates all variabled needed
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


# takes the input from the stock name a date and gets the data from the api
def get_data(stock_name, date_string):

    ticker = yf.Ticker(stock_name)
    data = ticker.history(start=date_string)

    # all data is formatted and ready to be visable on the website
    raw_data = {
        "high": round(data['High'][1], 2),
        "low": round(data['Low'][1], 2),
        "open": round(data['Open'][1], 2),
        "close": round(data['Close'][1], 2)
    }


    return raw_data
