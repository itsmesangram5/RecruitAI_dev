# login_model.py

from app import db
from models import User
from utils.GenerateToken import generate_jwt_token

class login_model():
    def login(self, body):
        data = body
        email = data.get('email')
        password = data.get('password')

        # Query the database to find the user with the provided email
        user = User.query.filter_by(email_id=email).first()

        if user and user.password == password:
            # If user exists and password matches, generate JWT token
            token = generate_jwt_token(user.user_id)
            response = {
                'message': 'Login Successful',
                'name': user.name,
                'role': user.role,
                'token': token  # No need to decode the token here
            }
            return response, 200
        else:
            # If user doesn't exist or password is incorrect
            response = {'message': 'Wrong Credentials'}
            return response, 401
