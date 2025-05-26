from marshmallow import Schema, fields


class SendMessageSchema(Schema):
    content = fields.Str(required=True, strict=True, error_messages={'required': 'Tin nhắn không được để trống',
                                                                     'strict': 'Tin nhắn phải là kiểu chữ'})
    sender = fields.Int(required=True, strict=True, error_messages={'required': 'Id người gửi không được để trống',
                                                                    'strict': 'Id người gửi phải là kiểu số'})
    reveive = fields.Int(required=True, strict=True, error_messages={'required': 'Id người nhận không được để trống',
                                                                    'strict': 'Id người nhận phải là kiểu số'})
