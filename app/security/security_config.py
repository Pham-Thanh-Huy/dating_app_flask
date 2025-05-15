from functools import wraps
from flask import request

from app.security.jwt_generation import verify_token
from app.utils.constant import Constant


def authenticate_api(f):
    @wraps(f)
    def authenticated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "").strip()

        if not auth_header or not auth_header.startswith("Bearer "):
            return {
                "message": "Bạn chưa cung cấp token hợp lệ! Vui lòng xác thực!",
                "code": Constant.API_STATUS.BAD_REQUEST
            }

        token = auth_header.split(' ')[1]

        data, err = verify_token(token)

        if err:
            return {
                "message": err,
                "code": Constant.API_STATUS.FORBIDDEN
            }

        return f(*args, **kwargs)

    return authenticated