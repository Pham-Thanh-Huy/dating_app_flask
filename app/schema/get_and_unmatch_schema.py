from marshmallow import Schema, fields


class GetAndUnmatchSchema(Schema):
    conversation_id = fields.Int(required=True, strict=True, error_messages={'required': 'id đoạn hội thoại không được để trống'})
    user_id = fields.Int(required=True, strict=True, error_messages={'required': 'id user không được để trống'})