from app import db
from models import JobPosting

class ViewJobModel:
    def get_all_jobs(self, user_id):
        try:
            # Query the JobPosting table to retrieve all job postings
            jobs = JobPosting.query.all()

            # If no jobs found, return None
            if not jobs:
                return None

            # Format the job postings data
            jobs_data = []
            for job in jobs:
                job_data = {
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
                    "job_description": job.job_desripation 
                }
                jobs_data.append(job_data)

            return jobs_data
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
