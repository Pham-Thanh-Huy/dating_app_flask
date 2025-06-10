from app.utils.constant import Constant


def internal_server_error_response() -> dict:
    return {
        "message": Constant.API_STATUS.INTERNAL_SERVER_ERROR_MESSAGE,
        "code": "9999",
        "http_status_code": Constant.API_STATUS.INTERNAL_SERVER_ERROR
    }
