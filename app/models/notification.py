from app import db


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        result = {}
        for column in self.__table__.columns:
            result[column.name] = getattr(self, column.name)
        return result
