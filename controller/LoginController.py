# LoginController.py
from app import app
from model.login_model import login_model
from flask import request, jsonify

obj = login_model()

@app.route('/login', methods=['POST'])
def login_controller():
    return obj.login(request.json)
