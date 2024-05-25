from app import app
from Service.ProcessResume import ProcessResume
from Service.AddScore import AddScore
from flask import request

obj = ProcessResume()
@app.route('/process', methods=['GET'])
def process_resume_controller():
    response=obj.process_resumes()
    return response

obj1 = AddScore()
@app.route('/addscore', methods=['GET'])
def add_score_controller():
    response=obj1.add_score()
    return response