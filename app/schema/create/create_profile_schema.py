from marshmallow import Schema, fields, validate
from app.models.profile import Gender

class CreateProfileSchema(Schema):
    name = fields.Str(required=True, error_messages={'required': 'Tên không đưọc để trống!'})
    user_id = fields.Int(required=True, error_messages={'required': 'không đưọc để trống id của user sẽ update!', 'type': 'user_id phải là kiểu số!'})
    email = fields.Email(required=True, error_messages={'required': 'email không đưọc để trống!', 'type': 'Vui lòng nhập đúng kiểu dữ liệu là email!'})
    avatar_url = fields.Str(required=True, error_messages={'required': 'avatar không được để trống!'})
    age = fields.Int(required=True, error_messages={'required': 'Tuổi không đưọc để trống!', 'type': 'tuổi phải là dữ liệu kiểu số!'})
    gender = fields.Str(required=True, validate=validate.OneOf(Gender.to_iterable(),
                                                               error="Giới tính vui lòng phải là 3 kiểu dữ liệu: 'male', 'female', 'other'!"),
                        error_messages={'required': 'Giới tính không đưọc để trống'})
    location = fields.Str(required=False)
    interests = fields.Raw(required=False)
