# DeleteResumeController.py

from flask import request, jsonify
from app import app
from model.deleteresumebyresume_id_model import DeleteResumeModel
from utils.GenerateToken import extract_user_id_from_token

obj = DeleteResumeModel()

@app.route('/deleteresumebyresume_id', methods=['DELETE'])
def delete_resume_controller():
    # Extracting user_id from the token
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"status": "error", "message": "Authorization token is missing or invalid"}), 401

    token = auth_header.split(" ")[1]
    user_id = extract_user_id_from_token(token)

    if user_id is None:
        return jsonify({"status": "error", "message": "Invalid or expired token"}), 403

    # Extracting resume_id from the request body
    data = request.get_json()
    if 'resume_id' not in data:
        return jsonify({"status": "error", "message": "resume_id is missing in the request body"}), 400

    resume_id = data['resume_id']

    # Deleting the resume
    result = obj.delete_resume(user_id, resume_id)

    if result:
        return jsonify({"status": "success", "message": "Resume deleted successfully."})
    else:
        return jsonify({"status": "error", "message": "Resume not found or could not be deleted."}), 404
