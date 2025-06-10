from marshmallow import Schema, fields, ValidationError

def validate_float(value):
    try:
        normalized = value.replace(',', '.')
        float(normalized)
    except (ValueError, AttributeError):
        raise ValidationError("Parameter value is invalid")  # Chuẩn lỗi 1004

class LocationSchema(Schema):
    lat = fields.Str(
        required=True,
        strict=True,
        validate=validate_float,
        error_messages={
            'required': "Parameter is not enough",  # 1002
            'invalid': "Parameter type is invalid"  # 1003
        }
    )
    lng = fields.Str(
        required=True,
        strict=True,
        validate=validate_float,
        error_messages={
            'required': "Parameter is not enough",
            'invalid': "Parameter type is invalid"
        }
    )
    radius = fields.Str(
        required=True,
        strict=True,
        validate=validate_float,
        error_messages={
            'required': "Parameter is not enough",
            'invalid': "Parameter type is invalid"
        }
    )
