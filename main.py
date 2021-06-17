from flask.templating import render_template_string
from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import sqlite3 
from sqlite3 import Error
app = Flask(__name__)

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/profile')
def profile():
  return render_template('profile.html')

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
    sql_query = '''INSERT INTO User (name, email, password) VALUES (?,?,?)'''
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
    login_valid = False
    while not login_valid:
      login_query = '''SELECT name, password FROM User WHERE name = (?) AND password = (?);'''
      cur = connection.cursor()
      cur.execute(login_query, (username, password))
      #if len(data) != 0:
        #login_valid = True 
    return redirect('/')

if __name__ == '__main__':
  app.run(port=8080, debug=True)