from app import app
from model.getallresumesbyApp_id_model import resume_model
from flask import request

obj = resume_model()

@app.route('/getallresumesbyApp_id', methods=['GET'])
def resume_controller():
    return obj.get_all_resumes(request)