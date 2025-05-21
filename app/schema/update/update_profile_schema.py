from marshmallow import Schema, fields, validate
from app.models.profile import Gender


class UpdateProfileSchema(Schema):
    name = fields.Str(required=False)
    user_id = fields.Int(required=True, error_messages={'required': 'không đưọc để trống id của user sẽ update!',
                                                        'type': 'user_id phải là kiểu số!'})
    email = fields.Email(required=False)
    avatar_url = fields.Str(required=False)
    age = fields.Int(required=False)
    gender = fields.Str(required=False, validate=validate.OneOf(Gender.to_iterable(),
                                                                error="Giới tính vui lòng phải là 3 kiểu dữ liệu: 'male', 'female', 'other'!"))
    location = fields.Str(required=False)
    interests = fields.Raw(required=False)
