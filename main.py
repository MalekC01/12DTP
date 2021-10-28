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
import hashlib
import re

app = Flask(__name__)

logged_in = None


#Connects website to the database
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


#This function is what commits my querys into my database,
#This function is called throughout my code.
def do_query(query, data=None, fetchall=False):
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
    #created key for session
    session['key'] = 'value'


@app.route('/get/')
def get():
    return session.get('key', 'not set')


#checks user has logged in
def check_logged_in():
    #checks to see if user is logged in,
    #determines soem functioanlity like what nav bar is shown.
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
    #once logged out is clicked session will end.
    #Means changes will be made to nav bar and what is avalible to the user
    session.pop('email', None)
    return render_template('logout.html', logged_in=logged_in)


@app.errorhandler(404)
def page_404(e):
    #if url is inavlid this will give the user an error message
    #telling them it is unavlible.
    logged_in = check_logged_in()
    return render_template('page_404.html', logged_in=logged_in), 404


#Home page
@app.route('/')
def home():
    logged_in = check_logged_in()
    print("logged in: " + str(logged_in))
    return render_template('home.html', logged_in=logged_in)


#Register Page
@app.route("/register")
def register():
    logged_in = check_logged_in()
    return render_template("register.html", logged_in=logged_in)


#Login page
@app.route("/login")
def login():
    return render_template("login.html", logged_in=logged_in)

#Registers a user and sends information to the database.
@app.route('/register', methods=['POST'])
def register_user():
    password_pass = None
    already_exists = True

    if request.method == "POST":
        name = request.form.get("Name")
        email = request.form.get("Email")
        password = request.form.get("Password")
        print("password: " + str(password))

        search_for_user = '''SELECT name FROM User
                 WHERE username_email = (?)'''
        check_not_already_registered = do_query(search_for_user, (email, ), True)
        if check_not_already_registered == []:
            #This check means that users are unable to break the website
            #Due to passwords being to long
            length_check = len(password)

            print(type(length_check))
            print("length: " + str(length_check))

            if length_check < 12 and length_check > 0:

                #list of special characters to compare against
                string_check= re.compile('[@_!#$%^&*()<>?/\|}{~:]') 
                if(string_check.search(password) == None): 

                    password_pass = True  

                    pre_hashed = bytes(password, 'utf-8')
                    hashed_password = int.from_bytes(
                    hashlib.sha256(pre_hashed).digest()[:8], 'little')

                    #Query that is used to add data from user into the database.
                    #Then uses the do query function.
                    sql_query = '''INSERT INTO User
                                (name, username_email, password)
                                VALUES (?, ?, ?)'''
                    do_query(sql_query, (name, email, hashed_password))   
                    print("password check: " + str(password_pass))
                    return redirect(url_for('login', password_pass=password_pass, logged_in=logged_in))

                else: 
                    password_pass = False
                    print("password check: " + str(password_pass))
                    return render_template('register.html', password_pass=password_pass, logged_in=logged_in)

            else:
                password_pass = False
                print("password check: " + str(password_pass))
                return render_template('register.html', password_pass=password_pass, logged_in=logged_in)
        else:
            already_exists = True
            print("account exists")
            return render_template('register.html', already_exists=already_exists, logged_in=logged_in)    
            




#Checks users input for login matches the information in the database.
@app.route("/login", methods=['POST'])
def login_check():
    if request.method == "POST":
        #takes data from the from on the login page.
        password = request.form.get("password")
        email = request.form.get("email")

        pre_hashed = bytes(password, 'utf-8')
        hashed_password = int.from_bytes(
            hashlib.sha256(pre_hashed).digest()[:8], 'little')

        #query that is used to search for the users data in the database.
        login_query = '''SELECT username_email,
                            password FROM User
                            WHERE username_email = (?)
                            AND password = (?);'''
        in_db = do_query(login_query, (email, hashed_password))
        #runs login check and returns
        #wheather or not this login is a match with data in database.
        if not in_db:
            logged_in = False
            return render_template("/login.html", logged_in=logged_in)
        else:
            logged_in = True
            #if login is true will then add the user to database
            #where it will be stored until logged out.
            session['email'] = email

            #finds the id of the user in the
            #database using the email gathered  from the form.
            find_id = '''SELECT id FROM User WHERE username_email = (?);'''
            uid = do_query(find_id, (session['email'], ))
            session['uid'] = uid[0]
            return render_template("/login.html", logged_in=logged_in)


@app.route("/favourites")
def favourites():
    favourite_stocks = None
    logged_in = check_logged_in()
    #runs query of what stocks the user has added to their favoruites,
    #then returns data which is then displayed to the user on the website.
    sql_query = '''SELECT stock_ticker FROM Favourites
                   WHERE id IN (SELECT sid FROM UserFav WHERE uid = ?);'''
    favourite_stocks = do_query(sql_query, (session['uid'], ), True)
    return render_template("favourites.html",
                           logged_in=logged_in,
                           favourite_stocks=favourite_stocks)


#Stock page and api, this is where the data is gathered
#and to be sent to the website where it is displayed to the user.
@app.route('/stocks', methods=["GET", "POST"])
def stock_data():

    in_fav = False
    logged_in = check_logged_in()

    stock.clear_data()

    #makes sure it session has most recently searched stock by the user.
    session.pop('stock_1', None)

    stock_exists = comparison_stock_exists()

    #creates all the varibles needed top be used for the data in the website.
    stock_valid = True
    date_valid = None
    find_data = None
    stock_name = None
    favourite = None
    info_for_graph = None
    description = None
    date = None

    if request.method == "POST":
        #info is gathered from users about what
        #stock they would like to see and what date.
        stock_name = request.form.get("Stock_name")
        date = request.form.get("data_date")
        stock_name = stock_name.upper()

        #checks the stock inputted by the user is a valid stock
        #and is able to be found by the api.
        stock_valid = stock.stock_is_valid(stock_name)

        #checks that the date entered by the user is valid.
        #Reasons may not be valid is on a weekend or other day the
        #market is closed or the stock was not created then.
        date_valid, date_string = stock.is_date_valid(date)

        #if both stock and date is valid runs function that will get the data.
        if stock_valid and date_valid:
            find_data = stock.get_data(stock_name, date_string)

            #checks all is correct and gets all information needed.
            #Creates session for stock name.
            session["stock_name"] = stock_name

            find_stock_id = '''SELECT id FROM Favourites
                               WHERE stock_ticker = (?)'''
            stock_id = do_query(find_stock_id, (session['stock_name'], ), True)
            if stock_id == []:
                sql_query = '''INSERT INTO Favourites
                               (stock_ticker) VALUES (?);'''
                stock_id = do_query(sql_query, (session['stock_name'], ))

            stock_id = do_query(find_stock_id, (session['stock_name'], ), True)

            session["stock_id"] = stock_id[0][0]

            session["stock_1"] = find_data
            stock_exists = comparison_stock_exists()
            in_fav = check_in_favourites()
            info_for_graph = data_for_graph(stock_name)
            description = get_description(stock_name)

    return render_template("stocks.html",
                           description=description,
                           info_for_graph=info_for_graph,
                           in_fav=in_fav,
                           stock_valid=stock_valid,
                           date_valid=date_valid,
                           find_data=find_data,
                           stock_name=stock_name,
                           favourite=favourite,
                           logged_in=logged_in,
                           stock_exists=stock_exists,
                           date=date)


def check_in_favourites():
    #querys database to find if stock entered
    #by the user is already in favoruties.
    #Determines what button is shown to the user.
    find_id = '''SELECT stock_ticker FROM Favourites
                 WHERE id IN
                 (SELECT sid FROM UserFav WHERE uid = ?)'''
    if logged_in:
        stocks = do_query(find_id, (session['uid'], ), True)
    else:
        return False

    stock_list = []

    for item in stocks:
        stock_list.append(item[0])

    if stock_list is not None and session['stock_name'] in stock_list:
        return True
    else:
        return False


#searches for the historic data to add to the graph.
def data_for_graph(stock_name):

    #using the api with all previous
    #information from user to get a final result.
    ticker = yf.Ticker(stock_name)
    hist = ticker.history(period="max")

    #puts data for the graph into a readable and formatable file.
    data = hist['Close'].to_csv()
    data_list = data.split()

    date_list = []
    value_list = []

    #seperates all value so they can then be turned into a graph.
    for item in data_list[1:]:
        items = item.split(',')
        date_list.append(items[0])
        value_list.append(float(items[1]))

    data_for_graph = [['Date', 'Price']]

    for i in range(len(date_list)):
        data_for_graph.append([date_list[i], value_list[i]])

    return data_for_graph


def get_description(stock_name):
    #uses api to get description by using the users input.
    ticker = yf.Ticker(stock_name)
    description_blurb = []
    blurb = ticker.info
    #only takes out the specfic part of the return from api that is needed.
    description = description_blurb.append(blurb['longBusinessSummary'])

    return description_blurb


@app.route('/remove_from_favourites')
def remove_from_favoruites():
    #query that is used if the user no longer
    #wants to have a stock in their favourites tab.
    remove_query = '''DELETE FROM UserFav WHERE uid = (?) AND sid = (?);'''
    do_query(remove_query, (session['uid'], session['stock_id']))

    return redirect('/profile')


@app.route('/add_to_favourites')
def add_to_favourites():

    #query used to insert wanted stock into database in realtion to the user.
    sql_query = '''INSERT INTO UserFav (uid, sid) VALUES (?, ?);'''
    do_query(sql_query, (session['uid'], session["stock_id"]))
    in_fav = check_in_favourites()

    return redirect('/')


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    sess = Session()
    sess.init_app(app)

    app.run(port=8080, debug=True)
