from app.utils.constant import Constant


def internal_server_error_response():
    return {
        "message": Constant.API_STATUS.INTERNAL_SERVER_ERROR_MESSAGE,
        "code": Constant.API_STATUS.INTERNAL_SERVER_ERROR
    }
