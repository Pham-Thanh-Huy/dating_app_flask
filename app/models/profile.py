import enum

import pytz

from app import db
from app.utils.constant import Constant


class Gender(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

    @classmethod
    def to_iterable(cls):
        return [member.value for member in cls]


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
    profile_image = db.relationship('ProfileImage', backref='profile')
    location_relation = db.relationship('Location', backref='location')

    def to_dict(self):
        result = {}
        # Đảm bảo rằng bạn đã lấy đối tượng datetime với múi giờ
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')

        for column in self.__table__.columns:
            value = getattr(self, column.name)

            if (column.name == "created_at" or column.name == "updated_at") and value is not None:
                # Chuyển đổi về múi giờ Việt Nam
                if value.tzinfo is None:  # Nếu datetime không có thông tin múi giờ
                    value = pytz.utc.localize(value)  # Giả sử là UTC, bạn có thể thay đổi theo cách khác nếu cần
                value = value.astimezone(vietnam_tz)

                # Sau khi chuyển đổi, format lại thời gian
                result[column.name] = value.strftime('%Y-%m-%d %H:%M:%S')

            elif isinstance(value, Gender):
                result[column.name] = value.name
            else:
                result[column.name] = value
        return result
