# RecruiterController.py

from flask import request, jsonify
from app import app ,db
from utils.GenerateToken import extract_user_id_from_token
from model.getjobbyrec_id_model import PostJobModel
from model.getalljobsbyApp_id_model import ViewJobModel
from model.deletejobbyjob_id_model import DeleteJobModel
from model.addjobbyrec_id_model import jobdescriptionform_model 
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from utils.GenerateToken import extract_user_id_from_token  
from models import Score, JobApplication, Applicant, Resume   




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
def getjob_controller():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Authorization token is missing or invalid"}), 401

    token = auth_header.split(" ")[1]
    rec_id = extract_user_id_from_token(token)
    if rec_id is None:
        return jsonify({"error": "Invalid or expired token"}), 401

    result = obj3.get_all_posts(rec_id)
    if result is None:
        return jsonify({"error": "No job postings found for this recruiter"}), 404

    return jsonify({"PostJob": result})

@app.route('/getjob_list_byrec_id', methods=['GET'])
def getjoblist_controller():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Authorization token is missing or invalid"}), 401

    token = auth_header.split(" ")[1]
    rec_id = extract_user_id_from_token(token)
    if rec_id is None:
        return jsonify({"error": "Invalid or expired token"}), 401

    result = obj3.get_all_postsList(rec_id)
    if result is None:
        return jsonify({"error": "No job postings found for this recruiter"}), 404

    return jsonify({"JobList": result})



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


@app.route('/selected_scores', methods=['POST'])
def get_selected_scores():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    user_id = extract_user_id_from_token(token)

    if not user_id:
        return jsonify({"error": "Invalid or missing token"}), 401

    data = request.get_json()

    try:
        no_of_students = data['noOfStudents']
        job_id = data['job_id']
        weights = {
            "Soft Skills": data['Soft Skills'],
            "Technical Skills": data['Technical Skills'],
            "Project Weightage": data['Project Weightage'],
            "Educational Marks": data['Educational Marks'],
            "Branch": data['Branch'],
            "College": data['College']
        }
    except KeyError as e:
        return jsonify({"error": f"Missing parameter: {str(e)}"}), 400

    # Fetching relevant data
    scores = Score.query.join(JobApplication).filter(JobApplication.job_id == job_id).all()

    if not scores:
        return jsonify({"error": "No scores found for the given job_id"}), 404

    # Calculate weighted scores
    student_scores = []
    for score in scores:
        weighted_total = (
            weights['Soft Skills'] * score.soft_skill +
            weights['Technical Skills'] * score.tech_skill +
            weights['Project Weightage'] * score.project +
            weights['Educational Marks'] * score.education +
            weights['Branch'] * score.branch +
            weights['College'] * score.clg
        )
        applicant_name = score.job_application.applicant.user.name

        student_scores.append({
            "applicant_name": applicant_name,
            "applicant_id": score.job_application.applicant_id,
            "resume_id": score.job_application.resume_id,
            "weighted_total": weighted_total,
            "Soft Skills" : score.soft_skill,
            "Technical Skills" : score.tech_skill,
            "Project" : score.project,
            "Educational Marks" : score.education,
            "Branch" : score.branch,
            "College" : score.clg
        })

    # Sort by weighted total and select top students
    top_students = sorted(student_scores, key=lambda x: x['weighted_total'], reverse=True)[:no_of_students]

    return jsonify(top_students), 200


