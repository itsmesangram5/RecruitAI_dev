# DeleteJobController.py

from flask import request, jsonify
from app import app
from model.deletejobbyjob_id_model import DeleteJobModel
from utils.GenerateToken import extract_user_id_from_token

obj = DeleteJobModel()

@app.route('/deletejobbyjob_id', methods=['DELETE'])
def delete_job_controller():
    # Extracting user_id from the token
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"status": "error", "message": "Authorization token is missing or invalid"}), 401

    token = auth_header.split(" ")[1]
    user_id = extract_user_id_from_token(token)

    if user_id is None:
        return jsonify({"status": "error", "message": "Invalid or expired token"}), 403

    # Extracting job_id from the request body
    data = request.get_json()
    if 'job_id' not in data:
        return jsonify({"status": "error", "message": "job_id is missing in the request body"}), 400

    job_id = data['job_id']

    # Deleting the job
    result = obj.delete_job(user_id, job_id)

    if result:
        return jsonify({"status": "success", "message": "Job deleted successfully."})
    else:
        return jsonify({"status": "error", "message": "Job not found or could not be deleted."}), 404
