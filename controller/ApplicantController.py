from app import app , db
from model.getallresumesbyApp_id_model import resume_model
from flask import request , jsonify
import os
from config import Config
from models import Applicant , Resume 
from werkzeug.utils import secure_filename
app.config.from_object(Config)
obj = resume_model() 

@app.route('/getallresumesbyApp_id', methods=['GET'])
def resume_controller():
    return obj.get_all_resumes(request)

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


