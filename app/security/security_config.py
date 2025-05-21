from functools import wraps
from flask import request, make_response

from app.security.jwt_generation import verify_token
from app.utils.constant import Constant


def authenticate_api(f):
    @wraps(f)
    def authenticated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "").strip()

        if not auth_header or not auth_header.startswith("Bearer "):
            return make_response({
                "message": "Bạn chưa cung cấp token xác thực hợp lệ! Vui lòng xác thực!",
                "code": Constant.API_STATUS.BAD_REQUEST
            }, Constant.API_STATUS.BAD_REQUEST)

        token = auth_header.split(' ')[1]

        data, err = verify_token(token)

        if err:
            return make_response({
                "message": err,
                "code": Constant.API_STATUS.FORBIDDEN
            }, Constant.API_STATUS.FORBIDDEN)

        return f(*args, **kwargs)

    return authenticated