from flask.templating import render_template_string
from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import sqlite3 
from sqlite3 import Error
import stock
print(stock.token)
print(stock.test("yes"))
app = Flask(__name__)

@app.route('/')
def home():
  return render_template('home.html')


@app.route('/stocks', methods = ["GET", "POST"]) 
def stock_data():
  result = None
  date_valid = None
  find_data = None
  if request.method == "POST":
    stock_name = request.form.get("Stock_name")
    date = request.form.get("data_date")

    print(stock_name, date)

    result = stock.stock_is_valid(stock_name)
    print(result)

    date_valid, date_string = stock.is_date_valid(date)
    print(date_valid)
    print(date_string)
  
    find_data = stock.get_data(stock_name, date_string)
    print(find_data)

  return render_template("stocks.html", result = result, date_valid = date_valid, find_data = find_data)

@app.route("/register")
def register():
  return render_template("register.html")

def create_connection(db_file):
  try:
    conn = sqlite3.connect(db_file)
    print(sqlite3.version)
  except Error as e:
    print(e)
  return conn

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

@app.route("/login")
def login():
 return render_template("login.html")
 
@app.route("/login", methods=['POST'])
def login_check():
  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")
  
    connection = create_connection('user_database.db')
    cur = connection.cursor()
    
    login_query = '''SELECT username_email, password FROM User WHERE username_email = (?) AND password = (?);'''
    cur.execute(login_query, (username, password))
    print((username, password))
    successful = None
    if not cur.fetchone():
      successful = False
      return render_template("/login.html", successful = successful)
    else:
      successful = True
      return render_template("/")
      

if __name__ == '__main__':
  app.run(port=8080, debug=True)