from app import db
from models import Resume, User, Applicant
from utils.GenerateToken import extract_user_id_from_token

class resume_model:
    def get_all_resumes(self, request):
        try:
            # Get the token from the Authorization header
            token = request.headers.get('Authorization').split('Bearer ')[1]
            # Extract user_id from the token
            user_id = extract_user_id_from_token(token)
            if user_id is None:
                return {"error": "Invalid or expired token"}, 401
            
            # Find the user and related applicant
            user = User.query.filter_by(user_id=user_id).first()
            if user is None:
                return {"error": "User not found"}, 404
            
            applicant = Applicant.query.filter_by(user_id=user_id).first()
            if applicant is None:
                return {"error": "Applicant not found"}, 404
            
            # Find resumes related to the applicant
            resumes = Resume.query.filter_by(applicant_id=applicant.applicant_id).all()
            # Construct the response JSON
            response = {"resumes": []}
            for resume in resumes:
                response["resumes"].append({
                    "resume_id": resume.resume_id,
                    "applicant_id": resume.applicant_id,
                    "resume_name": resume.resume_name
                })
            return response, 200
        except Exception as e:
            return {"error": str(e)}, 500
