import pytz

from app import db


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        result = {}
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')

        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if (column.name == "created_at" or column.name == "updated_at") and value is not None:
                if value.tzinfo is None:
                    value = pytz.utc.localize(value)
                value = value.astimezone(vietnam_tz)
                # Sau khi chuyển đổi, format lại thời gian
                result[column.name] = value.strftime('%Y-%m-%d %H:%M:%S')
            else: result[column.name] = getattr(self, column.name)
        return result
