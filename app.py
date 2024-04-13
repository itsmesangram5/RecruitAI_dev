from flask import Flask,render_template,request
from dotenv import load_dotenv  # Import the load_dotenv function
import config
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
from models import User


@app.cli.command()
def add():
    db.session.add(User(name='test'))
    db.session.commit()

#Check if the database connection is successful
@app.before_request
def check_db_connection():
    try:
        # Ping the database to check the connection
        db.engine.connect().close()
        logging.info("Connected to the database successfully!")
    except Exception as e:
        logging.error("Failed to connect to the database: %s", e)

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

if __name__ == '_main_':
    app.run(debug=True)

try:
    from controller import *
except Exception as e:
    print(e)