#%%
from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
import subprocess
import os
import sqlalchemy
SQLALCHEMY_SILENCE_UBER_WARNING = 1
SQLALCHEMY_WARN_20 = 0
import pandas as pd
import datetime
from sqlalchemy import text
import mysql.connector as msql
from mysql.connector import Error

db_host =  "34.175.28.179" # e.g. '127.0.0.1' ('172.17.0.1' if deployed to GAE Flex)
db_user =  "root" # e.g. 'my-db-user'
db_pass =   "%TGBnhy6" # e.g. 'my-db-password'
db_name =   "myflaskDB" # e.g. 'my-database'
db_port = 3306  # e.g. 3306

app = Flask(__name__)
app.secret_key = "session_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'my_secret_key'

from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:%TGBnhy6@34.175.28.179:3306/myflaskDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class User(db.Model):
    __tablename__ = 'table1'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User {self.username}>'




# with app.app_context():
#       db.create_all()
#       usr = User("sola","pp")
#       usr1 = User("bab","ppdf")
#       usr2 = User("df","fd")
#       db.session.add(usr1)
#       db.session.add(usr2)
#       db.session.commit()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/career')
def career():
      return render_template("career.html")


@app.route('/contact')
def contact():
    return 'Hello, World'

@app.route('/thankyou',methods = ["POST"])
def contactFormFilled():
    name = request.form["name"]
    return render_template("thankyou.html",name=name)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
   if request.method == 'POST':
       # retrieve the user's input from the form
       username = request.form['username']
       password = request.form['password']
       # create a new User object and add it to the database
       user = User(username= username, password=password)
       db.session.add(user)
       db.session.commit()
      
       return render_template('login.html')


   else:
       # render the signup form template
       return render_template('signup.html')
   
   

@app.route('/login')
def loginPage():
    return render_template("login.html")


@app.route("/handle-login", methods=["POST"])
def handleLogin():

    username = request.form["username"]
    password = request.form["password"]

    userFound = User.query.filter_by(username=username,password=password).first()   
    
    if (userFound): 
        session['username'] = username
        return redirect(url_for('profile'))
    else: 
        message = 'Invalid login credentials. Please try again.'
        return render_template('login.html', message=message)

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('loginPage'))


 
@app.route('/streamlit')
def streamlit():
    return render_template("streamlit.html")

@app.route('/run_streamlit')
def run_streamlit():
    subprocess.Popen(["streamlit","run","strr.py"])
    return ''




@app.route('/profile')
def profile():

   if ('username' in session):
       user_list = User.query.all()
       subprocess.Popen(["streamlit","run","strr.py"])
       return render_template('profile.html',users=user_list)
   else:
       return render_template('login.html',message="Hey you are not allowed here, you need to login!")

if __name__ == "__main__":
    app.run(debug=True,use_reloader=False,port = 4900)


# %%
