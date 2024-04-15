from app import app
from model.resume_model import resume_model
from flask import request

obj = resume_model()

@app.route('/resumes', methods=['GET'])
def resume_controller():
    return obj.get_all_resumes(request)