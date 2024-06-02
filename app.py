from flask import Flask, jsonify
from dotenv import load_dotenv  
import config
from flask_sqlalchemy import SQLAlchemy
import logging
from flask_migrate import Migrate
from flask_apscheduler import APScheduler
import uuid

# Load environment variables from .env file
load_dotenv()
logging.basicConfig(level=logging.INFO)
app = Flask(__name__, template_folder='view/templates', static_folder='view/static')

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

def check_db_connection():
    try:
        # Ping the database to check the connection
        db.engine.connect().close()
        logging.info("Connected to the database successfully!")
    except Exception as e:
        logging.error("Failed to connect to the database: %s", e)


app.config.from_object(config.Config)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

task_results = {}

# Define the function to be run by the scheduler
def process_resumes_task(task_id):
    try:
        logging.info(f"Task {task_id}: Process resumes task started")
        with app.app_context():
            # Instantiate ProcessResume and call the process_resumes method
            from Service.ProcessResume import ProcessResume
            obj = ProcessResume()
            result = obj.process_resumes()
            task_results[task_id] = result
            logging.info(f"Task {task_id}: Process resumes task completed")
    except Exception as e:
        logging.error(f"Task {task_id}: Error in process resumes task: {e}")
        task_results[task_id] = f"Error: {e}"


if __name__ == '__main__':
    print("Starting the app")
    logging.info("Starting the app")
    check_db_connection()
    app.run(debug=True)

try:
    from controller import *
except Exception as e:
    print(e)
