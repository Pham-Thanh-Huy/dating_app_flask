from marshmallow import Schema, fields

class GetListBlockSchema(Schema):
    user_id = fields.Int(
        required=True,
        strict=True,
        error_messages={
            'required': 'Parameter is not enough',
            'invalid': 'Parameter type is invalid'
        }
    )
    index = fields.Int(
        required=True,
        strict=True,
        error_messages={
            'required': 'Parameter is not enough',
            'invalid': 'Parameter type is invalid'
        }
    )
    count = fields.Int(
        required=True,
        strict=True,
        error_messages={
            'required': 'Parameter is not enough',
            'invalid': 'Parameter type is invalid'
        }
    )
