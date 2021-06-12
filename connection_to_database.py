"""from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import sqlite3 
from sqlite3 import Error

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn

connection = create_connection('user_database.db')

@app.route('/register', methods=['POST'])
def my_form():
    if request.method == "POST":
        name = request.form.get("Name")
        email = request.form.get("Username/Email")
        password = request.form.get("Password")
    try:
        sql_add_info = ("INSERT INTO user_database.User (name, email, password) VALUES (%s, %s, %s)")
        c.execute(sql_add_info,(name, email, password))
        connection.commit() 
        return redirect('/')
    except:
        print("Something went wrong saving your data. Please try agian.")"""


