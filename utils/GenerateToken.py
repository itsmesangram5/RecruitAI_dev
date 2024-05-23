import jwt
from datetime import datetime, timedelta

# Define your secret key for encoding and decoding JWTs
SECRET_KEY = 'my_secret_key'

def generate_jwt_token(user_id):
    """Generate a JWT token with a 1-day expiration."""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def extract_user_id_from_token(jwt_token):
    """Extract and verify the user_id from the JWT token."""
    try:
        # Decode the JWT token with the specified SECRET_KEY and algorithm
        decoded_token = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
        # Successfully decoded, extract the user_id
        user_id = decoded_token.get('user_id')
        return user_id
    except jwt.ExpiredSignatureError:
        print("The token has expired.")
        return None
    except jwt.InvalidTokenError:
        print("The token is invalid.")
        return None
    except jwt.PyJWTError as e:
        # Catch other JWT-related errors (covers broader exceptions)
        print(f"JWT error: {str(e)}")
        return None
    except Exception as e:
        # Generic exception handling (optional, for unexpected or non-JWT specific errors)
        print(f"An error occurred: {str(e)}")
        return None
