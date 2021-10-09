from flask.templating import render_template_string
import requests
from flask import Flask, render_template, url_for, request, redirect, session
from flask_session import Session
from datetime import datetime
import sqlite3 
from sqlite3 import Error
import stock
import yfinance as yf
import pandas as pd


test = "https://cloud.iexapis.com/stable/stock/aapl/chart/last-quarter?&token=pk_1649ada6b8c74aa1bd5761f73e9f6e58"
token =  "sk_6d3688ec98d6451bb686b8ac277dce59"

app = Flask(__name__)

logged_in = None



#Connects website to the database
def create_connection(db_file):
  try:
    conn = sqlite3.connect(db_file)
    print(sqlite3.version)
  except Error as e:
    print(e)
  return conn


def do_query(query, data = None, fetchall = False):
  conn = create_connection("user_database.db")
  cursor = conn.cursor()
  if data is None:
    cursor.execute(query)
  else:
    cursor.execute(query, data)
  conn.commit()
  results = cursor.fetchall() if fetchall else cursor.fetchone()
  conn.close()
  return results



#starts the session
@app.route('/set/')
def set():
  session['key'] = 'value'
  return 'ok'

@app.route('/get/')
def get():
  return session.get('key', 'not set')

#checks user has logged in 
def check_logged_in():
  if 'email' in session:
    return True
  return False

#makes sure form submission is valid
def comparison_stock_exists():
  if 'stock_1' in session:
    return True
  return False

#once session has started log out will end the session
@app.route('/logout')
def sign_out():
  session.pop('email', None)
  return render_template('logout.html', logged_in = logged_in)

@app.errorhandler(404)
def page_404(e):
  return render_template('page_404.html', logged_in = logged_in), 404

#Home page
@app.route('/')
def home():
  logged_in = check_logged_in()
  return render_template('home.html', logged_in = logged_in)

#Register Page
@app.route("/register")
def register():
  logged_in = check_logged_in()
  return render_template("register.html", logged_in = logged_in)

#Login page
@app.route("/login")
def login():
 return render_template("login.html", logged_in = logged_in)

#Profile page
@app.route("/profile")
def profile():
  return render_template("profile.html",  logged_in = logged_in)


#Registers a user and sends information to the database
@app.route('/register', methods=['POST'])
def my_form():
  register_user = None
  
  if request.method == "POST":
    name = request.form.get("Name")
    email = request.form.get("Email")
    password = request.form.get("Password")
    sql_query = '''INSERT INTO User (name, username_email, password) VALUES (?, ?, ?)'''
    do_query(sql_query,(name, email, password))
  return redirect('/')



#Checks users input for login matches the information in the database
@app.route("/login", methods=['POST'])
def login_check():
  if request.method == "POST":
    password = request.form.get("password")
    email = request.form.get("email")
 
    
    login_query = '''SELECT username_email, password FROM User WHERE username_email = (?) AND password = (?);'''
    in_db = do_query(login_query, (email, password))
    if not in_db:
      logged_in = False
      return render_template("/login.html", logged_in = logged_in)
    else:
      logged_in = True
      session['email'] = email

      find_id = '''SELECT id FROM User WHERE username_email = (?);'''
      uid = do_query(find_id, (session['email'],))
      session['uid'] = uid[0]
      return render_template("/login.html", logged_in = logged_in)

<<<<<<< HEAD
#Profile page
@app.route("/profile")
def profile():
  logged_in = check_logged_in()
  return render_template("profile.html",  logged_in = logged_in)
=======

>>>>>>> 06b60b2825e65a809610b017199bbb95789a9e4c
  

@app.route("/favourites")
def favourites():
  favourite_stocks = None
  logged_in = check_logged_in()
  sql_query = '''SELECT stock_name FROM Favourites WHERE uid = ?;'''
  favourite_stocks = do_query(sql_query, (session['uid'],), True)
  print(favourite_stocks)
  return render_template("favourites.html", logged_in = logged_in, favourite_stocks = favourite_stocks)


#Stock page and api
@app.route('/stocks', methods = ["GET", "POST"]) 
def stock_data():

  in_fav = False
  logged_in = check_logged_in()
  print(logged_in)

  stock.clear_data()

  session.pop('stock_1', None)

  print(session)

  stock_exists = comparison_stock_exists()

  stock_valid = True
  date_valid = None
  find_data = None
  stock_name = None
  favourite = None
  info_for_graph = None
  description = None

  if request.method == "POST":
    stock_name = request.form.get("Stock_name")
    date = request.form.get("data_date")
    stock_name = stock_name.upper()

    stock_valid = stock.stock_is_valid(stock_name)

    date_valid, date_string = stock.is_date_valid(date)
  
    if  stock_valid and date_valid:
      find_data = stock.get_data(stock_name, date_string)

      session["stock_name"] = stock_name
      session["stock_1"] = find_data
      stock_exists = comparison_stock_exists()

      in_fav = check_in_favourites()
      info_for_graph = data_for_graph(stock_name)
      description = get_description(stock_name)

  return render_template("stocks.html", description = description, info_for_graph = info_for_graph, in_fav = in_fav, stock_valid = stock_valid, date_valid = date_valid, find_data = find_data, stock_name = stock_name, favourite = favourite, logged_in = logged_in, stock_exists = stock_exists)


def check_in_favourites():
  find_id = '''SELECT stock_name FROM Favourites WHERE uid = (?);'''
  stocks = do_query(find_id, (session['uid'],))

  if stocks is not None and session['stock_name'] in stocks:
    return True
  return False
#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

def data_for_graph(stock_name):
    
  ticker = yf.Ticker(stock_name)
  print("data for graph")
  hist = ticker.history(period="max")

  data = hist['Close'].to_csv()
  data_list = data.split()

  date_list = []
  value_list = []

  for item in data_list[1:]:
      items = item.split(',')
      date_list.append(items[0])
      value_list.append(float(items[1]))

  data_for_graph = [['Date', 'Price']]

  for i in range(len(date_list)):
      data_for_graph.append([date_list[i], value_list[i]])

  return data_for_graph

def get_description(stock_name):

  ticker = yf.Ticker(stock_name)
  print("description")
  description_blurb = []
  blurb = ticker.info
  description = description_blurb.append(blurb['longBusinessSummary'])

  return description_blurb
  

@app.route('/favourite_toggle')
def favourite_toggle():

  
  
  return redirect('/')

@app.route('/remove_from_favourites')
def remove_from_favoruites():

  remove_query = '''DELETE FROM Favourites WHERE uid = (?) AND stock_name = (?);'''
  remove_stock = do_query(remove_query, (session['uid'], session['stock_name']))

  return redirect('/profile', logged_in = logged_in)



@app.route('/add_to_favourites')
def add_to_favourites():

  sql_query = '''INSERT INTO Favourites (uid, stock_name) VALUES (?, ?);'''
  do_query(sql_query, (session['uid'], session["stock_name"]))
  
  return redirect('/')



if __name__ == '__main__': 
  app.secret_key = 'super secret key'
  app.config['SESSION_TYPE'] = 'filesystem'

  sess = Session()
  sess.init_app(app)

  app.run(port=8080, debug=True)