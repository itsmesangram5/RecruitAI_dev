# models.py

from app import db
from sqlalchemy import LargeBinary

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    email_id = db.Column(db.Text)
    phone = db.Column(db.Text)
    password = db.Column(db.Text)
    role = db.Column(db.Text)
     
    #this is called as string representation which can be used as bellow 
    def __repr__(self):
        return f"<User(user_id={self.user_id}, name={self.name}, email_id={self.email_id}, phone={self.phone}, role={self.role})>"
    
"""

How to use above string representation 

    # Create an instance of the class
user = User(user_id=1, name='John', email_id='john@example.com', phone='1234567890', role='admin')

# Call __repr__ explicitly
print(user.__repr__())  # Output: <User(user_id=1, name=John, email_id=john@example.com, phone=1234567890, role=admin)>

# Alternatively, you can simply use the object in a print statement
print(user)  # Output: <User(user_id=1, name=John, email_id=john@example.com, phone=1234567890, role=admin)>
"""




class Applicant(db.Model):
    __tablename__ = 'applicants'

    applicant_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), unique=True)
    
    # Define one-to-one relationship with User table
    user = db.relationship('User', backref=db.backref('applicant', uselist=False))

    def __repr__(self):
        return f"<Applicant(applicant_id={self.applicant_id}, user_id={self.user_id})>"


class Resume(db.Model):
    __tablename__ = 'resumes'

    resume_id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicants.applicant_id'))

    resume_name = db.Column(db.Text, nullable=False)
    branch = db.Column(db.Text)
    passout_yr = db.Column(db.Integer)
    clg_10 = db.Column(db.Text)
    marks_10 = db.Column(db.Numeric(5, 2))
    clg_12 = db.Column(db.Text)
    marks_12 = db.Column(db.Numeric(5, 2))
    clg_engg = db.Column(db.Text)
    marks_engg = db.Column(db.Numeric(5, 2))
    exp_title1 = db.Column(db.Text)
    duration1 = db.Column(db.Text)
    exp_title2 = db.Column(db.Text)
    duration2 = db.Column(db.Text)
    exp_title3 = db.Column(db.Text)
    duration3 = db.Column(db.Text)
    project_title1 = db.Column(db.Text)
    p_tech1 = db.Column(db.Text)
    project_title2 = db.Column(db.Text)
    p_tech2 = db.Column(db.Text)
    project_title3 = db.Column(db.Text)
    p_tech3 = db.Column(db.Text)
    tech_skills = db.Column(db.Text)
    soft_skills = db.Column(db.Text)

    def __repr__(self):
        return f"<Resume(resume_id={self.resume_id}, applicant_id={self.applicant_id}, resume_name={self.resume_name})>"
    
class Recruiter(db.Model):
    __tablename__ = 'recruiters'

    recruiter_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), unique=True)

    user = db.relationship('User', backref=db.backref('recruiter', uselist=False))

    def __repr__(self):
        return f"<Recruiter(recruiter_id={self.recruiter_id}, user_id={self.user_id})>"


class JobPosting(db.Model):
    __tablename__ = 'job_postings'

    job_id = db.Column(db.Integer, primary_key=True)
    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiters.recruiter_id'))

    job_title = db.Column(db.Text)
    branch = db.Column(db.Text)
    passout_yr = db.Column(db.Integer)
    marks_10 = db.Column(db.Numeric(5, 2))
    marks_12 = db.Column(db.Numeric(5, 2))
    marks_engg = db.Column(db.Numeric(5, 2))
    exp_title = db.Column(db.Text)
    exp_tech = db.Column(db.Text)
    project_tech = db.Column(db.Text)
    tech_skills = db.Column(db.Text)
    soft_skills = db.Column(db.Text)
    ctc = db.Column(db.Numeric(5, 2))
    positions = db.Column(db.Integer)
    last_date_to_apply = db.Column(db.Date)
    company_name = db.Column(db.Text)
    job_desripation= db.Column(db.Text)

    def __repr__(self):
        return f"<JobPosting(job_id={self.job_id}, recruiter_id={self.recruiter_id}, job_title={self.job_title}, company_name={self.company_name})>"
    
class JobApplication(db.Model):
    __tablename__ = 'job_applications'

    job_application_id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job_postings.job_id'))
    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiters.recruiter_id'))
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicants.applicant_id'))
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.resume_id'))
    applied_date = db.Column(db.Date)
    status = db.Column(db.Text)

    # Define relationships
    job_posting = db.relationship('JobPosting', backref=db.backref('job_applications', lazy=True))
    recruiter = db.relationship('Recruiter', backref=db.backref('job_applications', lazy=True))
    applicant = db.relationship('Applicant', backref=db.backref('job_applications', lazy=True))
    resume = db.relationship('Resume', backref=db.backref('job_applications', lazy=True))

    def __repr__(self):
        return f"<JobApplication(job_application_id={self.job_application_id}, job_id={self.job_id}, recruiter_id={self.recruiter_id}, applicant_id={self.applicant_id}, resume_id={self.resume_id}, applied_date={self.applied_date}, status={self.status})>"

class Score(db.Model):
    __tablename__ = 'scores'

    score_id = db.Column(db.Integer, primary_key=True)
    job_application_id = db.Column(db.Integer, db.ForeignKey('job_applications.job_application_id'))

    education = db.Column(db.Numeric(5, 2))
    branch = db.Column(db.Numeric(5, 2))
    clg = db.Column(db.Numeric(5, 2))
    experience = db.Column(db.Numeric(5, 2))
    project = db.Column(db.Numeric(5, 2))
    soft_skill = db.Column(db.Numeric(5, 2))
    overall = db.Column(db.Numeric(5, 2))
    tech_skill = db.Column(db.Numeric(5, 2))
    
    job_application = db.relationship('JobApplication', backref=db.backref('scores', lazy=True))
    
    def __repr__(self):
        return f"<Score(marks_id={self.marks_id}, job_application_id={self.job_application_id}, overall={self.overall})>"

class Ranking(db.Model):
    __tablename__ = 'rankings'

    ranking_id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job_postings.job_id'))
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicants.applicant_id'))
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.resume_id'))
    rank = db.Column(db.Integer)

    job_posting = db.relationship('JobPosting', backref=db.backref('rankings', lazy=True))
    applicant = db.relationship('Applicant', backref=db.backref('rankings', lazy=True))
    resume = db.relationship('Resume', backref=db.backref('rankings', lazy=True))
    
    def __repr__(self):
        return f"<Ranking(ranking_id={self.ranking_id}, job_id={self.job_id}, applicant_id={self.applicant_id}, resume_id={self.resume_id}, rank={self.rank})>"
