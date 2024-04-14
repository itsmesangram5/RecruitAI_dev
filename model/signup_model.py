from flask import jsonify
from app import db
from models import User
from utils.GenerateToken import generate_jwt_token

class signup_model():
    def signup(self, body):
        data = body
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone')
        role = data.get('role')

        # Check if user with the same email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "Email already exists"}), 400

        user = User(name=name, email=email, password=password, phone=phone, role=role)
        db.session.add(user)
        db.session.commit()

        # Generate JWT token
        token = generate_jwt_token(user.user_id)

        response = {
            'name': name,
            'email': email,
            'phone': phone,
            'role': role,
            'token': token
        }

        if role == 'Applicant' or role == 'Recruiter':
            return jsonify(response), 201
        else:
            return jsonify({'error': 'Invalid role'}), 400

    def login(self, body):
        data = body
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            # You may want to return more information in the response, such as user details or a token
            return jsonify({"message": "Login successful."}), 200
        else:
            return jsonify({"error": "Invalid email or password."}), 401
