from app import db
from models import JobPosting, Recruiter
import sqlalchemy

class PostJobModel:
    def get_all_posts(self, user_id):
        try:
            recruiter = db.session.query(Recruiter).filter_by(user_id=user_id).first()
            if not recruiter:
                return None

            # Fetch job postings associated with the recruiter
            job_postings = db.session.query(JobPosting).filter_by(recruiter_id=recruiter.recruiter_id).all()

            # Check if job_postings is empty or None
            if not job_postings:
                return None

            result = []
            for job in job_postings:
                result.append({
                    "job_id":job.job_id,
                    "job_title": job.job_title,
                    "branch": job.branch,
                    "passout_yr": job.passout_yr,
                    "marks_10": float(job.marks_10),
                    "marks_12": float(job.marks_12),
                    "marks_engg": float(job.marks_engg),
                    "exp_title": job.exp_title,
                    "exp_tech": job.exp_tech,
                    "project_tech": job.project_tech,
                    "tech_skills": job.tech_skills,
                    "soft_skills": job.soft_skills,
                    "ctc": float(job.ctc),
                    "positions": job.positions,
                    "last_date_to_apply": job.last_date_to_apply,
                    "company_name": job.company_name,
                    "job_description": job.job_desripation  # Typo corrected here
                })

            return result
        except sqlalchemy.exc.SQLAlchemyError as e:
            print(f"Database error: {e}")
            return None
        
    def get_all_postsList(self, user_id):
        try:
            recruiter = db.session.query(Recruiter).filter_by(user_id=user_id).first()
            if not recruiter:
                return None

            # Fetch job postings associated with the recruiter
            job_postings = db.session.query(JobPosting).filter_by(recruiter_id=recruiter.recruiter_id).all()

            # Check if job_postings is empty or None
            if not job_postings:
                return None

            result = []
            for job in job_postings:
                result.append({
                    "job_title": job.job_title,
                    "job_id": job.job_id
                })

            return result
        except sqlalchemy.exc.SQLAlchemyError as e:
            print(f"Database error: {e}")
            return None
