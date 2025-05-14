from marshmallow import Schema, fields, validate

class RegisterLoginSchema(Schema):
    username = fields.Str(required=True,
                          validate=validate.Length(min=5, max=15, error="Tên đăng nhập phải từ 5-15 ký tự"),
                          error_messages={'required': 'Tên đăng nhập không để trống!'})
    password = fields.Str(required=True,
                          validate=validate.Regexp(r'^(?=.*\d)(?=.*[A-Z])(?=.*[!@#$%^&*()]).{8,20}$',
                                                   error="Mật khẩu phải từ 8-20 ký tự và bao gồm 1 chữ in hoa, 1 ký tự đặc biệt, 1 số bất kì"),
                          error_messages={'required': 'Mật khẩu  không được để trống!'})
