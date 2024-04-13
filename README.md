To run 

python -m venv venv
./venv/Scripts/activate
pip install -r requirements.txt
flask run

To create Database 
CREATE DATABASE `my_database` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

To add Tables
flask db migrate -m "Commit Message"


To apply changes 
flask db upgrade

If Migration file is not present 
flask db init