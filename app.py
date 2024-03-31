from flask import Flask , render_template , request
app=Flask(__name__,template_folder='view/templates')

@app.route("/")
def welcome():
    return render_template('index.html')

@app.route("/home")
def home():
    return " Home my "

from controller import *