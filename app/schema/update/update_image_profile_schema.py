from marshmallow import Schema, fields

class UpdateImageProfileSchema(Schema):
    image = fields.Raw(
        required=True,
        error_messages={
            'required': "Parameter is not enough",
            'invalid': "Parameter type is invalid"
        }
    )
    user_id = fields.Int(
        required=True,
        error_messages={
            'required': "Parameter is not enough",
            'invalid': "Parameter type is invalid",
            'type': "Parameter type is invalid"
        }
    )
