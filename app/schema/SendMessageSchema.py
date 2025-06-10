from marshmallow import Schema, fields

class SendMessageSchema(Schema):
    content = fields.Str(
        required=True,
        strict=True,
        error_messages={
            'required': 'Parameter is not enough',
            'invalid': 'Parameter type is invalid',
            'strict': 'Parameter type is invalid'
        }
    )
    sender = fields.Int(
        required=True,
        strict=True,
        error_messages={
            'required': 'Parameter is not enough',
            'invalid': 'Parameter type is invalid',
            'strict': 'Parameter type is invalid'
        }
    )
    reveive = fields.Int(
        required=True,
        strict=True,
        error_messages={
            'required': 'Parameter is not enough',
            'invalid': 'Parameter type is invalid',
            'strict': 'Parameter type is invalid'
        }
    )
