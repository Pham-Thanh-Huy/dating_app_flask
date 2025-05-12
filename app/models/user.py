from enum import unique

from sqlalchemy.orm import backref

from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.Date, nullable=False)
    updated_at = db.Columnt(db.DateTime, nullable=True)

    # ------> ADD RELATION SHIP
    profile = db.relationship('Profile', backref='user', uselist=False, lazy=True) # One To One
    interaction = db.relationship('Interaction', backref='user', lazy=False)
