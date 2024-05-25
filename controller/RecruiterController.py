# RecruiterController.py

from flask import request, jsonify
from app import app
from utils.GenerateToken import extract_user_id_from_token
from model.getjobbyrec_id_model import PostJobModel
from model.getalljobsbyApp_id_model import ViewJobModel
from model.deletejobbyjob_id_model import DeleteJobModel
from model.addjobbyrec_id_model import jobdescriptionform_model 




obj4 = DeleteJobModel()
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
    result = obj4.delete_job(user_id, job_id)

    if result:
        return jsonify({"status": "success", "message": "Job deleted successfully."})
    else:
        return jsonify({"status": "error", "message": "Job not found or could not be deleted."}), 404


obj3 = PostJobModel()
@app.route('/getjobbyrec_id', methods=['GET'])
def postjob_controller():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Authorization token is missing or invalid"}), 401

    token = auth_header.split(" ")[1]
    user_id = extract_user_id_from_token(token)
    if user_id is None:
        return jsonify({"error": "Invalid or expired token"}), 401

    result = obj3.get_all_posts(user_id)
    if result is None:
        return jsonify({"error": "No job postings found for this recruiter"}), 404

    return jsonify({"PostJob": result})

obj2 = ViewJobModel()
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
        jobs = obj2.get_all_jobs(user_id)

        # Handle case where no job postings found
        if jobs is None:
            return jsonify({"error": "No job postings found"}), 404

        # Return job postings
        return jsonify({"jobs": jobs}), 200

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": str(e)}), 500
    
obj1 = jobdescriptionform_model()
@app.route('/addjobbyrec_id', methods=['POST'])
def jobdescriptionform_controller():
    if request.headers.get('Authorization'):
        jwt_token = request.headers.get('Authorization').split()[1]
        return obj1.jobdescriptionform(jwt_token, request.json)
    else:
        return jsonify({"error": "Authorization header not provided"}), 401
