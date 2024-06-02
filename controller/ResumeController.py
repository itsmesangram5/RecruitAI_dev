from app import app
from Service.AddScore import AddScore
from app import app
from flask import request , jsonify
import uuid


@app.route('/process', methods=['GET'])
def process_resume_controller():
    from app import scheduler, process_resumes_task
    task_id = str(uuid.uuid4())
    scheduler.add_job(id=task_id, func=process_resumes_task, args=[task_id], replace_existing=True)
    return jsonify({'task_id': task_id}), 202

@app.route('/task_status/<task_id>', methods=['GET'])
def task_status(task_id):
    from app import task_results
    if task_id in task_results:
        return jsonify({'task_id': task_id, 'status': 'completed', 'result': task_results[task_id]})
    else:
        return jsonify({'task_id': task_id, 'status': 'pending'}), 202

obj1 = AddScore()
@app.route('/addscore', methods=['GET'])
def add_score_controller():
    response=obj1.add_score()
    return response