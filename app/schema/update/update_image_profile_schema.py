from marshmallow import Schema, fields


class UpdateImageProfileSchema(Schema):
    image = fields.Raw(type="files", required=True, error_messages={'required': "Hình ảnh không được để trống"})
    user_id = fields.Int(required=True, error_messages={'required': 'không đưọc để trống id của user sẽ update!',
                                                        'type': 'user_id phải là kiểu số!'})