# models.py

from app import db

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    email_id = db.Column(db.Text)
    phone = db.Column(db.Text)
    password = db.Column(db.Text)
    role = db.Column(db.Text)

    def __repr__(self):
        return f"<User(user_id={self.user_id}, name={self.name}, email_id={self.email_id}, phone={self.phone}, role={self.role})>"
