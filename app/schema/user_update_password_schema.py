from marshmallow import Schema, fields, validate, validates, ValidationError

class UserUpdatePasswordSchema(Schema):
    old_password = fields.Str(required=True, error_messages={'required': "Mật khẩu cũ không được để trống!"})
    user_id = fields.Int(required=True, error_messages={'required': "không đưọc để trống id của user sẽ update!"})
    new_password = fields.Str(required=True,
                          validate=validate.Regexp(r'^(?=.*\d)(?=.*[A-Z])(?=.*[!@#$%^&*()]).{8,20}$',
                                                   error="Mật khẩu mới phải từ 8-20 ký tự và bao gồm 1 chữ in hoa, 1 ký tự đặc biệt, 1 số bất kì"),
                          error_messages={'required': 'Mật khẩu mới không được để trống!'})

    @validates("user_id")
    def validate_user_id(self, value):
        if isinstance(value, str):
            raise ValidationError("user_id phải là 1 số!")