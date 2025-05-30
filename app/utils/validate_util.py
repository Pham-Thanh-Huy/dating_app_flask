from flask import make_response

from app.utils.constant import Constant


def validate_param_type_int(param_name, param_value):
    if not param_value:
        return None, make_response({
            "code": Constant.API_STATUS.BAD_REQUEST,
            "message": f"Vui lòng truyền param {param_name}"
        }, Constant.API_STATUS.BAD_REQUEST)

    try:
        return int(param_value), None
    except ValueError:
        return None, make_response({
            "code": Constant.API_STATUS.BAD_REQUEST,
            "message": f"{param_name} phải là số nguyên"
        }, Constant.API_STATUS.BAD_REQUEST)
