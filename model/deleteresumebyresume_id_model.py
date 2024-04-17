# delete_resume_model.py

from app import db
from models import Resume, Applicant

class DeleteResumeModel:
    def delete_resume(self, user_id, resume_id):
        try:
            # Check if the applicant owns the resume
            owns_resume = db.session.query(Resume.query.join(Applicant).filter(Applicant.user_id == user_id, Resume.resume_id == resume_id).exists()).scalar()

            if not owns_resume:
                return False

            # Delete the resume
            resume = Resume.query.get(resume_id)
            db.session.delete(resume)
            db.session.commit()

            return True
        except Exception as e:
            print(f"Error: {str(e)}")
            return False
