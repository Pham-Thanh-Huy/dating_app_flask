from marshmallow import Schema, fields, validate

class AddInteractionSchema(Schema):
    profile_id = fields.Int(
        required=True,
        strict=True,
        error_messages={
            'required': "Parameter is not enough",
            'invalid': "Parameter type is invalid",
            'type': "Parameter type is invalid"
        }
    )
    user_id = fields.Int(
        required=True,
        strict=True,
        error_messages={
            'required': "Parameter is not enough",
            'invalid': "Parameter type is invalid",
            'type': "Parameter type is invalid"
        }
    )
    is_like = fields.Int(
        required=True,
        strict=True,
        validate=validate.OneOf(
            [0, 1],
            error="Parameter value is invalid"
        ),
        error_messages={
            'required': "Parameter is not enough",
            'invalid': "Parameter type is invalid",
            'type': "Parameter type is invalid"
        }
    )
