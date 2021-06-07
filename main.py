from flask import Flask, render_template
from flask.templating import render_template_string


app = Flask(__name__)


@app.route('/')
def home():
  return render_template('home.html')

@app.route("/register")
def login():
  return render_template("register.html")

@app.route("/profile")
def profile():
  return render_template("profile.html")


if __name__ == '__main__':
  app.run(port=8080, debug=True)