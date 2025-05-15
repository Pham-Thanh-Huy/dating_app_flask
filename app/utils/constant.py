class Constant:
    ADD_USER_SUCCESS = "Thêm người dùng thành công!"
    USERNAME_OR_PASSWORD_INCORRECT = "Tài khoản hoặc mật khẩu không đúng !"
    LOGIN_SUCCESS = "Đăng nhập thành công!"
    TOKEN_INVALID= "Token không hợp lệ!"
    TOKEN_EXPIRED = "Token hết hạn!"
    class API_STATUS:
        INTERNAL_SERVER_ERROR = 500
        SUCCESS = 200
        NOT_FOUND = 404
        NOT_PERMITTED = 403
        BAD_REQUEST = 400
        FORBIDDEN = 403

        INTERNAL_SERVER_ERROR_MESSAGE = "Internal Server Error!"
        SUCCESS_MESSAGE = "Success!"
        NOT_FOUND_MESSAGE = "Not Found!"
        NOT_PERMITTED_MESSAGE = "Not Permitted!"
        BAD_REQUEST_MESSAGE = "Bad Request!"
        FORBIDDEN_MESSAGE = "Forbidden!"