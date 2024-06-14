from app import db
from models import JobPosting, Applicant, JobApplication
from datetime import datetime

class JobApplicationModel:
    def apply_for_job(self, job_id, applicant_id, resume_id):
        # Check if the job exists
        job = JobPosting.query.filter_by(job_id=job_id).first()
        if not job:
            return None, "Job not found"

        # Check if the applicant exists
        applicant = Applicant.query.filter_by(applicant_id=applicant_id).first()
        if not applicant:
            return None, "Applicant not found"

        # Create a new job application
        new_job_application = JobApplication(
            job_id=job_id,
            recruiter_id=job.recruiter_id,
            applicant_id=applicant_id,
            resume_id=resume_id,
            applied_date=datetime.utcnow(),
            status='Applied'
        )

        # Save to database
        db.session.add(new_job_application)
        db.session.commit()

        return {
            "job_application_id": new_job_application.job_application_id,
            "job_id": new_job_application.job_id,
            "recruiter_id": new_job_application.recruiter_id,
            "applicant_id": new_job_application.applicant_id,
            "resume_id": new_job_application.resume_id,
            "applied_date": new_job_application.applied_date.strftime("%Y-%m-%d %H:%M:%S"),
            "status": new_job_application.status
        }, None
        
        
    def getAllJobApplications(self, applicant_id):
        try:
            jobapplications = JobApplication.query.filter_by(applicant_id=applicant_id).all()
            if not jobapplications:
                return "Job Applications not found"
            
            jobapplications_data = []
            for jobapplication in jobapplications:
                jobapplication_data = {
                    "job_application_id": jobapplication.job_application_id,
                    "job_id": jobapplication.job_id,
                    "recruiter_id": jobapplication.recruiter_id,
                    "applicant_id": jobapplication.applicant_id,
                    "resume_id": jobapplication.resume_id,
                    "status": jobapplication.status,
                }
                jobapplications_data.append(jobapplication_data)

            return jobapplications_data
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

