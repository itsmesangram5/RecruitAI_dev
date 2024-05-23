from flask import Flask
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



if __name__ == '_main_':
    app.run(debug=True)

try:
    from controller import *
except Exception as e:
    print(e)