import enum
from enum import unique
from app import db

class Gender(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    avatar_url = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    location = db.Column(db.String(255))
    interests = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    profile_image =  db.relationship('ProfileImage', backref='profile', dynamic=True)
