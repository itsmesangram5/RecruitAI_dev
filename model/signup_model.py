from flask import jsonify
from app import db
from models import User
from utils.GenerateToken import generate_jwt_token

class signup_model():
   def signup(self,body):
    data = body
    name = data.get('name')
    email = data.get('email')  # Assuming 'email' is the input name
    password = data.get('password')
    phone = data.get('phone')
    role = data.get('role')

    user = User(name=name, email_id=email, password=password, phone=phone, role=role)  # Using 'email_id' instead of 'email'
    db.session.add(user)
    db.session.commit()

    # Generate JWT token
    # You'll need to implement this function, see step 2
    token = generate_jwt_token(user.user_id)

    response = {
        'name': name,
        'email': email,
        'password': password,  # Note: This should not be returned in a real scenario
        'phone': phone,
        'role': role,
        'token': token
    }

    if role == 'Applicant':
        return jsonify(response), 201, {'Location': '/Applicant.html'}
    elif role == 'Recruiter':
        return jsonify(response), 201, {'Location': '/Recruiter.html'}
    else:
        return jsonify({'error': 'Invalid role'}), 400