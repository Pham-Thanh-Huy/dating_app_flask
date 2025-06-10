from marshmallow import Schema, fields, validate

class RegisterLoginSchema(Schema):
    username = fields.Str(
        required=True,
        validate=validate.Length(min=5, max=15, error="Parameter value is invalid"),
        error_messages={'required': 'Parameter is not enough'}
    )
    password = fields.Str(
        required=True,
        validate=validate.Regexp(
            r'^(?=.*\d)(?=.*[A-Z])(?=.*[!@#$%^&*()]).{8,20}$',
            error="Parameter value is invalid"
        ),
        error_messages={'required': 'Parameter is not enough'}
    )
