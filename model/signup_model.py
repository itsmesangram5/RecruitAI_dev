from flask import jsonify
from app import db
from models import User, Applicant, Recruiter
from utils.GenerateToken import generate_jwt_token

class signup_model():
    def signup(self, body):
        data = body
        name = data.get('name')
        email = data.get('email')  
        password = data.get('password')
        phone = data.get('phone')
        role = data.get('role')

        # Check if a user with the same email or phone number already exists
        existing_user = User.query.filter((User.email_id == email) | (User.phone == phone)).first()
        if existing_user:
            # If a user with the same email or phone number already exists, return an error response
            return jsonify({'error': 'User already exists. Please login with existing credentials.'}), 400

        # If no existing user found, proceed to create a new user
        user = User(name=name, email_id=email, password=password, phone=phone, role=role)
        db.session.add(user)
        db.session.commit()

        # Generate JWT token
        token = generate_jwt_token(user.user_id)

        response = {
            'name': name,
            'email': email,
            'password': password,  # Note: This should not be returned in a real scenario
            'phone': phone,
            'role': role,
            'token': token
        }

        # Create an entry in the Applicant or Recruiter table based on the role
        if role == 'Applicant':
            applicant = Applicant(user_id=user.user_id)
            db.session.add(applicant)
            db.session.commit()
            response['applicant_id'] = applicant.applicant_id
            return jsonify(response), 201
        elif role == 'Recruiter':
            recruiter = Recruiter(user_id=user.user_id)
            db.session.add(recruiter)
            db.session.commit()
            response['recruiter_id'] = recruiter.recruiter_id
            return jsonify(response), 201
        else:
            return jsonify({'error': 'Invalid role'}), 400
