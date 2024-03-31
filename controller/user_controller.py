from app import app
from model.user_model import *
from flask import request

obj=user_model()
@app.route("/user/signup")
def user_signup_controller():
    return obj.user_signup_model()

@app.route("/user/get")
def user_get_controller():
    return obj.user_get()

@app.route("/user/add", methods=["POST"])
def user_add_controller():
    #print(request.form)
    return obj.user_add(request.form)
