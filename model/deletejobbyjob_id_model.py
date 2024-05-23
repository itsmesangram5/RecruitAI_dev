# deletejob_model.py

from app import db
from models import JobPosting, Recruiter

class DeleteJobModel:
    def delete_job(self, user_id, job_id):
        try:
            # Find recruiter_id from the user and job_posting table relation using user_id
            recruiter_id = db.session.query(Recruiter.recruiter_id).filter_by(user_id=user_id).scalar()

            if not recruiter_id:
                return False

            # Check if the job_id exists for the given recruiter_id
            job = JobPosting.query.filter_by(recruiter_id=recruiter_id, job_id=job_id).first()

            if not job:
                return False

            # Delete the job
            db.session.delete(job)
            db.session.commit()

            return True
        except Exception as e:
            print(f"Error: {str(e)}")
            return False
