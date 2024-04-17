from flask import jsonify
from app import db
from models import Recruiter , JobPosting

from utils.GenerateToken import generate_jwt_token
from utils.GenerateToken import extract_user_id_from_token

class jobdescriptionform_model():
    def jobdescriptionform(self, jwt_token, body):
        user_id = extract_user_id_from_token(jwt_token)

        # Find recruiter_id using user_id
        recruiter = Recruiter.query.filter_by(user_id=user_id).first()

        if recruiter:
            # Assuming payload is sent as JSON in the request body
            payload = body

            # Save job posting using recruiter_id and payload
            job_posting = JobPosting(
                recruiter_id=recruiter.recruiter_id,
                job_title=payload.get('job_title'),
                branch=payload.get('branch'),
                passout_yr=payload.get('passout_yr'),
                marks_10=payload.get('marks_10'),
                marks_12=payload.get('marks_12'),
                marks_engg=payload.get('marks_engg'),
                exp_title=payload.get('exp_title'),
                exp_tech=payload.get('exp_tech'),
                project_tech=payload.get('project_tech'),
                tech_skills=payload.get('tech_skills'),
                soft_skills=payload.get('soft_skills'),
                ctc=payload.get('ctc'),
                positions=payload.get('positions'),
                last_date_to_apply=payload.get('last_date_to_apply'),
                company_name=payload.get('company_name'),
                job_desripation=payload.get('job_desripation')
            )

            db.session.add(job_posting)
            db.session.commit()

            return jsonify({"message": "Job posting successfully created."}), 200
        else:
            return jsonify({"error": "Recruiter not found."}), 404
