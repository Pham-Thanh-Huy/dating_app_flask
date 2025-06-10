from marshmallow import Schema, fields, validate, validates, ValidationError

class UserUpdatePasswordSchema(Schema):
    old_password = fields.Str(
        required=True,
        error_messages={'required': "Parameter is not enough", 'invalid': "Parameter type is invalid"}
    )
    user_id = fields.Int(
        required=True,
        error_messages={'required': "Parameter is not enough", 'invalid': "Parameter type is invalid"}
    )
    new_password = fields.Str(
        required=True,
        validate=validate.Regexp(
            r'^(?=.*\d)(?=.*[A-Z])(?=.*[!@#$%^&*()]).{8,20}$',
            error="Parameter value is invalid"
        ),
        error_messages={'required': "Parameter is not enough", 'invalid': "Parameter type is invalid"}
    )

    @validates("user_id")
    def validate_user_id(self, value):
        # Kiểm tra thêm nếu value kiểu str, trả lỗi kiểu dữ liệu
        if isinstance(value, str):
            raise ValidationError("Parameter type is invalid")
