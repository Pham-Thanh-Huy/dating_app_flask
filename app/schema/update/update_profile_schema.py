from marshmallow import Schema, fields, validate, ValidationError
from app.models.profile import Gender

class UpdateProfileSchema(Schema):
    name = fields.Str(required=False)

    user_id = fields.Int(
        required=True,
        error_messages={
            'required': "Parameter is not enough",
            'invalid': "Parameter type is invalid",
            'type': "Parameter type is invalid"
        }
    )

    email = fields.Email(
        required=False,
        error_messages={
            'invalid': "Parameter value is invalid"
        }
    )

    avatar_url = fields.Str(required=False)

    age = fields.Int(
        required=False,
        error_messages={
            'invalid': "Parameter type is invalid",
            'type': "Parameter type is invalid"
        }
    )

    gender = fields.Str(
        required=False,
        validate=validate.OneOf(
            Gender.to_iterable(),
            error="Parameter value is invalid"
        )
    )

    location = fields.Str(required=False)

    interests = fields.Raw(required=False)
