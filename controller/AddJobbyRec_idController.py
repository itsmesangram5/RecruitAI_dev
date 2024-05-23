from app import app
from model.addjobbyrec_id_model import jobdescriptionform_model 
from flask import request

obj = jobdescriptionform_model()

@app.route('/addjobbyrec_id', methods=['POST'])
def jobdescriptionform_controller():
    if request.headers.get('Authorization'):
        jwt_token = request.headers.get('Authorization').split()[1]
        return obj.jobdescriptionform(jwt_token, request.json)
    else:
        return jsonify({"error": "Authorization header not provided"}), 401
