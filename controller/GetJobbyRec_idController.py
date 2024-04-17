from flask import request, jsonify, abort
from models import JobPosting
from utils.GenerateToken import extract_user_id_from_token
from app import app
from model.getjobbyrec_id_model import PostJobModel

obj = PostJobModel()

@app.route('/getjobbyrec_id', methods=['GET'])
def postjob_controller():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Authorization token is missing or invalid"}), 401

    token = auth_header.split(" ")[1]
    user_id = extract_user_id_from_token(token)
    if user_id is None:
        return jsonify({"error": "Invalid or expired token"}), 401

    result = obj.get_all_posts(user_id)
    if result is None:
        return jsonify({"error": "No job postings found for this recruiter"}), 404

    return jsonify({"PostJob": result})
