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

@app.route("/login")
def login():
  return render_template("login.html")

if __name__ == '__main__':
  app.run(port=8080, debug=True)