from marshmallow import Schema, fields, ValidationError

def validate_float(value):
    try:
        normalized = value.replace(',', '.')
        float(normalized)
    except (ValueError, AttributeError):
        raise ValidationError("Giá trị phải là một số hợp lệ.")

class LocationSchema(Schema):
    lat = fields.Str(
        required=True,
        strict=True,
        validate=validate_float,
        error_messages={'required': "lat không được để trống"}
    )
    lng = fields.Str(
        required=True,
        strict=True,
        validate=validate_float,
        error_messages={'required': "lng không được để trống"}
    )
    radius = fields.Str(
        required=True,
        strict=True,
        validate=validate_float,
        error_messages={'required': "radius không được để trống"}
    )
