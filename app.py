from flask import Flask

app=Flask(__name__)

@app.route("/")
def welcome():
    return "Hello word Sangram"

@app.route("/home")
def home():
    return " Home my "

from controller import *