from app import app , db
from model.getallresumesbyApp_id_model import resume_model
from flask import request , jsonify
import os
from utils.GenerateToken import extract_user_id_from_token
from config import Config
from models import Applicant , Resume , JobApplication , JobPosting
from werkzeug.utils import secure_filename
from model.deleteresumebyresume_id_model import DeleteResumeModel
from utils.GenerateToken import extract_user_id_from_token
from model.job_application_model import JobApplicationModel
app.config.from_object(Config)

obj = resume_model() 
@app.route('/getallresumesbyApp_id', methods=['GET'])
def resume_controller():
    return obj.get_all_resumes(request)

from model.deleteresumebyresume_id_model import DeleteResumeModel
obj1 = DeleteResumeModel()

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
    result = obj1.delete_resume(user_id, resume_id)

    if result:
        return jsonify({"status": "success", "message": "Resume deleted successfully."})
    else:
        return jsonify({"status": "error", "message": "Resume not found or could not be deleted."}), 404




@app.route('/upload', methods=['POST'])
def upload_file():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Authorization header is missing'}), 401

    jwt_token = auth_header.split(" ")[1]  # Assuming the format is 'Bearer <token>'
    user_id = extract_user_id_from_token(jwt_token)
    if not user_id:
        return jsonify({'error': 'Invalid or expired token'}), 401

    applicant = Applicant.query.filter_by(user_id=user_id).first()
    if not applicant:
        return jsonify({'error': 'Applicant not found'}), 404

    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        new_resume = Resume(applicant_id=applicant.applicant_id, resume_name=filename)
        db.session.add(new_resume)
        db.session.commit()

        new_filename = f"resume_{new_resume.resume_id}.pdf"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        file.save(file_path)

        return jsonify({'message': f'File successfully uploaded as {new_filename}'}), 200
    else:
        return jsonify({'error': 'File is not a PDF'}), 400

from Service.AddScore import AddScore
add_score_instance = AddScore()

@app.route('/add_score/<int:jobapplication_id>', methods=['GET'])
def add_score(jobapplication_id):
    return add_score_instance.add_score(jobapplication_id)


job_app_model = JobApplicationModel()


@app.route('/apply', methods=['POST'])
def apply_job():
    # Extract JSON data from the request
    data = request.get_json()

    # Extract resume_id and job_id from JSON data
    resume_id = data.get('resume_id')
    job_id = data.get('job_id')

    # Extract JWT token from Authorization header
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        return jsonify({'message': 'Authorization header is missing'}), 401

    # Extract user_id from JWT token
    token = auth_header.split(" ")[1]
    user_id = extract_user_id_from_token(token)
    if user_id is None:
        return jsonify({'message': 'Invalid token or token has expired'}), 401

    # Fetch applicant_id from the database using user_id
    applicant_id = fetch_applicant_id(user_id)
    if applicant_id is None:
        return jsonify({'message': 'User is not an applicant'}), 403

    # Fetch recruiter_id from the database using job_id
    recruiter_id = fetch_recruiter_id(job_id)
    if recruiter_id is None:
        return jsonify({'message': 'Job not found or invalid job_id'}), 404

    # Create a new JobApplication entry
    job_application = JobApplication(
        job_id=job_id,
        recruiter_id=recruiter_id,
        applicant_id=applicant_id,
        resume_id=resume_id,
        status="Applied"
    )

    # Add the new entry to the database
    db.session.add(job_application)
    db.session.commit()

    return jsonify({'message': 'Job application submitted successfully'}), 201



@app.route('/getalljobapplications', methods=['GET'])
def getalljobapplications_controller():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Authorization token is missing or invalid"}), 401

    token = auth_header.split(" ")[1]
    user_id = extract_user_id_from_token(token)
    if user_id is None:
        return jsonify({"error": "Invalid or expired token"}), 401
    
    applicant_id=fetch_applicant_id(user_id)
    result = job_app_model.getAllJobApplications(applicant_id)
    if result is None:
        return jsonify({"error": "No Job Applications found for this recruiter"}), 404
    return jsonify({"Job Applications": result})
    

def fetch_applicant_id(user_id):
    # Query the Applicant table to fetch applicant_id using user_id
    applicant = Applicant.query.filter_by(user_id=user_id).first()
    if applicant:
        return applicant.applicant_id
    else:
        return None

def fetch_recruiter_id(job_id):
    # Query the JobPosting table to fetch recruiter_id using job_id
    job_posting = JobPosting.query.get(job_id)
    if job_posting:
        return job_posting.recruiter_id
    else:
        return None