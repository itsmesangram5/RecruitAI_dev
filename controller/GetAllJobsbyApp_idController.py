from flask import request, jsonify
from app import app
from model.getalljobsbyApp_id_model import ViewJobModel
from utils.GenerateToken import extract_user_id_from_token

obj = ViewJobModel()

@app.route('/getalljobsbyapp_id', methods=['GET'])
def view_jobs_controller():
    # Extract token from Authorization header
    auth_header = request.headers.get('Authorization')

    # Check if token exists and has the correct format
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Authorization token is missing or invalid"}), 401

    # Extract user_id from the token
    token = auth_header.split(" ")[1]
    user_id = extract_user_id_from_token(token)

    # Handle invalid or expired token
    if user_id is None:
        return jsonify({"error": "Invalid or expired token"}), 403

    try:
        # Retrieve job postings for the user
        jobs = obj.get_all_jobs(user_id)

        # Handle case where no job postings found
        if jobs is None:
            return jsonify({"error": "No job postings found"}), 404

        # Return job postings
        return jsonify({"jobs": jobs}), 200

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": str(e)}), 500
