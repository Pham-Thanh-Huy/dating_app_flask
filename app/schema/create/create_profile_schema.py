from marshmallow import Schema, fields, validate
from app.models.profile import Gender

class CreateProfileSchema(Schema):
    name = fields.Str(
        required=True,
        error_messages={
            'required': 'Parameter is not enough',
            'invalid': 'Parameter type is invalid',
            'type': 'Parameter type is invalid'
        }
    )
    user_id = fields.Int(
        required=True,
        error_messages={
            'required': 'Parameter is not enough',
            'invalid': 'Parameter type is invalid',
            'type': 'Parameter type is invalid'
        }
    )
    email = fields.Email(
        required=True,
        error_messages={
            'required': 'Parameter is not enough',
            'invalid': 'Parameter value is invalid',
            'type': 'Parameter type is invalid'
        }
    )
    avatar_url = fields.Str(
        required=True,
        error_messages={
            'required': 'Parameter is not enough',
            'invalid': 'Parameter type is invalid',
            'type': 'Parameter type is invalid'
        }
    )
    age = fields.Int(
        required=True,
        error_messages={
            'required': 'Parameter is not enough',
            'invalid': 'Parameter type is invalid',
            'type': 'Parameter type is invalid'
        }
    )
    gender = fields.Str(
        required=True,
        validate=validate.OneOf(
            Gender.to_iterable(),
            error='Parameter value is invalid'
        ),
        error_messages={
            'required': 'Parameter is not enough',
            'invalid': 'Parameter type is invalid',
            'type': 'Parameter type is invalid'
        }
    )
    location = fields.Str(required=False)
    interests = fields.Raw(required=False)
