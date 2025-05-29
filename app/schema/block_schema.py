from marshmallow import Schema, fields


class GetListBlockSchema(Schema):
    user_id = fields.Int(required=True, error_messages={'required': 'id của user không được để trống'})
    index = fields.Int(required=True, error_messages={'required': 'index không được để trống'})
    count = fields.Int(required=True, error_messages={'required': 'count không được để trống'})
