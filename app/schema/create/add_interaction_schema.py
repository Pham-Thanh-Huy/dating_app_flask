from marshmallow import Schema, fields, validate


class AddInteractionSchema(Schema):
    profile_id = fields.Int(required=True, error_messages={'required': "profile id không được để trống!"})
    user_id = fields.Int(required=True, error_messages={'required': "user id không được để trống!"})
    is_like = fields.Integer(required=True, validate=validate.OneOf([0, 1],
                                                                    error="is_like chỉ được chọn 0 hoặc 1 và là kiểu dữ liệu số!"),
                             error_messages={'required': 'is like không được để trống!'})
