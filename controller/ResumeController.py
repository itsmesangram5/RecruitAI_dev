from app import app
from model.ProcessResume import ProcessResume
from flask import request

obj = ProcessResume()


@app.route('/process', methods=['GET'])
def process_resume_controller():
    response=obj.process_resumes()
    return response
