from flask.templating import render_template_string
import requests
from flask import Flask, render_template, url_for, request, redirect, session
from flask_session import Session
from datetime import datetime
import sqlite3 
from sqlite3 import Error
import stock

token =  "pk_bc4de76560684c36bff00ec3f7802ae9"

app = Flask(__name__)


logged_in = None

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
 return render_template("/login.html", logged_in = logged_in)






#Registers a user and sends information to the database
@app.route('/register', methods=['POST'])
def my_form():
  
  if request.method == "POST":
    name = request.form.get("Name")
    email = request.form.get("Email")
    password = request.form.get("Password")
  connection = create_connection('user_database.db')
  try:
    sql_query = '''INSERT INTO User (name, username_email, password) VALUES (?,?,?)'''
    cur = connection.cursor()
    cur.execute(sql_query, (name, email, password))
    connection.commit()
  except:
    print("Something went wrong saving your data. Please try agian.")

  finally:
    if connection:
      connection.close()
  return redirect('/')



#Connects website to the database
def create_connection(db_file):
  try:
    conn = sqlite3.connect(db_file)
    print(sqlite3.version)
  except Error as e:
    print(e)
  return conn





#Checks users input for login matches the information in the database
@app.route("/login", methods=['POST'])
def login_check():
  if request.method == "POST":
    password = request.form.get("password")
    email = request.form.get("email")
    connection = create_connection('user_database.db')
    cur = connection.cursor()
    
    login_query = '''SELECT username_email, password FROM User WHERE username_email = (?) AND password = (?);'''
    cur.execute(login_query, (email, password))
    if not cur.fetchone():
      logged_in = False
      return render_template("/login.html", logged_in = logged_in)
    else:
      logged_in = True
      session['email'] = email

      find_id = '''SELECT id FROM User WHERE username_email = (?);'''
      cur = connection.cursor()
      c_uid = cur.execute(find_id, (session['email'],))
      uid = c_uid.fetchone()
      connection.commit()
      session['uid'] = uid[0]
      return render_template("/login.html", logged_in = logged_in)





#Profile page
@app.route("/profile")
def profile():
  favourite_stocks = None
  logged_in = check_logged_in()

  connection = create_connection('user_database.db')
  sql_query = '''SELECT stock_name FROM Favourites WHERE uid = ?;'''
  cur = connection.cursor()
  stocks = cur.execute(sql_query, (session['uid'],))
  favourite_stocks = stocks.fetchall()
  connection.commit()
  return render_template("profile.html", logged_in = logged_in, favourite_stocks = favourite_stocks)




#Stock page and api
@app.route('/stocks', methods = ["GET", "POST"]) 
def stock_data():

  in_fav = False
  logged_in = check_logged_in()

  stock.clear_data()

  session.pop('stock_1', None)

  stock_exists = comparison_stock_exists()

  result = None
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
    print("stock name" + str(stock_name))

    result = stock.stock_is_valid(stock_name)

    date_valid, date_string = stock.is_date_valid(date)
  
    if result == True and date_valid == True:
      find_data = stock.get_data(stock_name, date_string)

      session["stock_name"] = stock_name
      session["stock_1"] = find_data
      stock_exists = comparison_stock_exists()

      in_fav = check_in_favourites()
      print("in fav: " + str(in_fav))
      info_for_graph = get_data_for_graph(stock_name)
      description = get_description(stock_name)

  return render_template("stocks.html", description = description, info_for_graph = info_for_graph, in_fav = in_fav, result = result, date_valid = date_valid, find_data = find_data, stock_name = stock_name, favourite = favourite, logged_in = logged_in, stock_exists = stock_exists)


def check_in_favourites():
  find_id = '''SELECT stock_name FROM Favourites WHERE uid = (?);'''
  connection = create_connection('user_database.db')
  cur = connection.cursor()
  c_stocks = cur.execute(find_id, (session['uid'],))
  stocks = c_stocks.fetchone()
  connection.commit()  
  

  if stocks is not None and session['stock_name'] in stocks:
    return True
  return False


def get_data_for_graph(stock_name):
  test_stock =  f"https://cloud.iexapis.com/stable/stock/{stock_name}/chart/last-quarter?&token={token}"
  date_close = []
  date_for_graph = []

  result = requests.get(test_stock).json()
  for result in result:
    date_close.append(result['close'])

  find_date = requests.get(test_stock).json()
  for find_date in find_date:
    date_for_graph.append(find_date['date']) 

  data_for_graph = [['Date', 'Price']]

  for i in range(60):
    data_for_graph.append([date_for_graph[i], date_close[i]])
  return data_for_graph


def get_description(stock_name):
  description_url = f"https://cloud.iexapis.com/stable/stock/{stock_name}/company?&token={token}"
  decription = requests.get(description_url).json()

  decription_blurb = []
  decription_blurb.append(decription['description'])

  return decription_blurb
  

@app.route('/remove_from_favourites')
def remove_from_favoruites():
  
  print(session['email'])
  connection = create_connection('user_database.db')
  print("remove from favourite is running.")
  try:
    remove_query = '''DELETE FROM Favourites WHERE uid = (?) AND stock_name = (?);'''
    cur = connection.cursor()
    remove_stock = cur.execute(remove_query, (session['uid'], session['stock_name']))
    connection.commit() 

  except:
    print("Something went wrong removing from favourites. Please try agian.")

  finally:
    if connection:
      connection.close()
  return redirect('/profile')


@app.route('/add_to_favourites')
def add_to_favourites():
  print("Favourites Running")
  connection = create_connection('user_database.db')
  try:
    refresh = True
    sql_query = '''INSERT INTO Favourites (uid, stock_name) VALUES (?, ?);'''
    cur = connection.cursor()
    cur.execute(sql_query, (session['uid'], session["stock_name"]))
    connection.commit()
    
  except:
    print("Something went adding to favourites. Please try agian.")

  finally:
    if connection:
      connection.close()
  return redirect('/stock', refresh = refresh)




if __name__ == '__main__': 
  app.secret_key = 'super secret key'
  app.config['SESSION_TYPE'] = 'filesystem'

  sess = Session()
  sess.init_app(app)

  app.run(port=8080, debug=True)