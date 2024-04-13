from flask import Flask,render_template,request
from dotenv import load_dotenv  # Import the load_dotenv function
import os
import config
from controller import*
from flask_sqlalchemy import SQLAlchemy
import logging
from flask_migrate import Migrate


# Load environment variables from .env file
load_dotenv()
logging.basicConfig(level=logging.INFO)
app=Flask(__name__,template_folder='view/templates',static_folder='view/static')

# Set configuration variables from config module
app.config.from_object(config.Config)

# Initialize SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# db.init_app(app)
from models import User
# class User(db.Model):
#     __tablename__ = 'users'

#     user_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.Text)
#     email_id = db.Column(db.Text)
#     phone = db.Column(db.Text)
#     password = db.Column(db.Text)
#     role = db.Column(db.Text)

#     def __repr__(self):
#         return f"<User(user_id={self.user_id}, name={self.name}, email_id={self.email_id}, phone={self.phone}, role={self.role})>"

@app.cli.command()
def add():
    """Add test user."""
    db.session.add(User(name='test'))
    db.session.commit()



# Check if the database connection is successful
# @app.before_request
# def check_db_connection():
#     try:
#         # Ping the database to check the connection
#         db.engine.connect().close()
#         logging.info("Connected to the database successfully!")
#     except Exception as e:
#         logging.error("Failed to connect to the database: %s", e)

@app.route("/")
def welcome():
    return render_template('index.html')

@app.route('/signup')
def signup():
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

if __name__ == '_main_':
    app.run(debug=True)

