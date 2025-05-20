from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.Date, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)

    # ------> ADD RELATION SHIP
    profile = db.relationship('Profile', backref='user', uselist=False, lazy=True) # One To One
    interaction = db.relationship('Interaction', backref='user', lazy=True)
    notification = db.relationship('Notification', backref='user', lazy=True)
    messages = db.relationship('Message', backref='user', lazy=True)