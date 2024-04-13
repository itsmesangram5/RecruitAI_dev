from app import app
from model.signup_model import signup_model
from flask import request

obj = signup_model()


@app.route('/signup', methods=['POST'])
def signup_controller():
    return obj.signup(request.json)