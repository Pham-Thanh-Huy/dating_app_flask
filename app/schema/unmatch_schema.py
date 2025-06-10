from marshmallow import Schema, fields

class UnmatchSchema(Schema):
    conversation_id = fields.Int(
        required=True,
        strict=True,
        error_messages={
            'required': 'Parameter is not enough',
            'invalid': 'Parameter type is invalid'
        }
    )
    user_id = fields.Int(
        required=True,
        strict=True,
        error_messages={
            'required': 'Parameter is not enough',
            'invalid': 'Parameter type is invalid'
        }
    )
