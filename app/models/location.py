from enum import unique

from app import db


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.String(255), nullable=False)
    lng = db.Column(db.String(255), nullable=False)

    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), unique = True, nullable = False)
