from flask import make_response

from app.utils.constant import Constant


def validate_param_type_int(param_name, param_value):
    if not param_value:
        return None, make_response({
            "code": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH,
            "message": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH_MESSAGE
        }, Constant.API_STATUS.BAD_REQUEST)

    try:
        return int(param_value), None
    except ValueError:
        return None, make_response({
            "code": Constant.API_STATUS.PARAMETER_TYPE_IS_INVALID,
            "message": Constant.API_STATUS.PARAMETER_TYPE_IS_INVALID_MESSAGE
        }, Constant.API_STATUS.BAD_REQUEST)




def parse_validation_error(e):
    messages = e.messages

    if any("Parameter is not enough" in msg for msgs in messages.values() for msg in msgs):
        return {
            "message": "Parameter is not enough",
            "http_status_code": "400",
            "code": "1002"
        }

    if any("Parameter type is invalid" in msg for msgs in messages.values() for msg in msgs):
        return {
            "message": "Parameter type is invalid",
            "http_status_code": "400",
            "code": "1003"
        }

    return {
        "message": "Parameter value is invalid",
        "http_status_code": "400",
        "code": "1004"
    }