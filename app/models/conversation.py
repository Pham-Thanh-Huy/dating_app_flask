from app import db

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_one_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_two_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime)

    message = db.relationship('Message', backref='conversation', lazy='dynamic')