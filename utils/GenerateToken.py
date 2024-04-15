import jwt
from datetime import datetime, timedelta

SECRET_KEY = 'my_key'

def generate_jwt_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

import jwt

def extract_user_id_from_token(jwt_token):
    try:
        # Decode the JWT token
        decoded_token = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
        # Extract the user_id from the decoded token
        user_id = decoded_token.get('user_id')
        return user_id
    except jwt.ExpiredSignatureError:
        # Handle expired token
        return None
    except jwt.InvalidTokenError:
        # Handle invalid token
        return None
