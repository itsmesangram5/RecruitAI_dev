from app import app
from flask import render_template

@app.route("/")
def welcome():
    return render_template('index.html')

@app.route('/signup_view')
def signup_view():
    return render_template('signup.html')

@app.route('/applicant')
def applicant_home():
    return render_template('applicant.html')  

@app.route('/applications')
def applications():
    return render_template('applications.html')

@app.route('/uploadresume')
def uploadresume():
    return render_template('uploadresume.html')

@app.route('/jobs')
def jobs():
    return render_template('jobs.html')

@app.route('/selectresume')
def selectresume():
    return render_template('selectresume.html')

@app.route('/recruiter')
def recruiter_home():
    return render_template('recruiter.html')  


@app.route('/postedjobs')
def postjob():
    return render_template('postedjobs.html')

@app.route('/jobdescriptionform')
def jobdescriptionform():
    return render_template('jobdescriptionform.html')

@app.route('/shortlisting')
def shortlisting():
    return render_template('shortlisting.html')

@app.route('/result')
def result():
    return render_template('result.html')