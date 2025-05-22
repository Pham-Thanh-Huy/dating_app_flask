from app import db

class Interaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_like = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))