import pytz


class Constant:
    ADD_USER_SUCCESS = "Đăng ký người dùng thành công!"
    USERNAME_OR_PASSWORD_INCORRECT = "Tài khoản hoặc mật khẩu không đúng !"
    LOGIN_SUCCESS = "Đăng nhập thành công!"
    TOKEN_INVALID = "Token không hợp lệ!"
    ERROR_TO_PARSE_TOKEN = "Lỗi khi parse token!"
    TOKEN_EXPIRED = "Token hết hạn!"
    DELETE_SUCCESS = "Xóa thành công!"
    CHANGE_PASSWORD_SUCCESS = "Đổi mật khẩu thành công!"

    LOCATION_URL = "https://nominatim.openstreetmap.org/search"
    # LOCATION_URL = "https://google.com"

    class API_STATUS:
        INTERNAL_SERVER_ERROR = "500"
        SUCCESS = "200"
        NOT_FOUND = "404"
        NOT_PERMITTED = "403"
        BAD_REQUEST = "400"
        FORBIDDEN = "403"

        INTERNAL_SERVER_ERROR_MESSAGE = "Internal Server Error!"
        SUCCESS_MESSAGE = "Success!"
        NOT_FOUND_MESSAGE = "Not Found!"
        NOT_PERMITTED_MESSAGE = "Not Permitted!"
        BAD_REQUEST_MESSAGE = "Bad Request!"
        FORBIDDEN_MESSAGE = "Forbidden!"


        # ---- > OK
        OK = "1000"
        OK_MESSAGE = "OK"

        # -----> Bài viết không tồn tại
        POST_IS_NOT_EXISTED = "9992"
        POST_IS_NOT_EXISTED_MESSAGE = "Post is not existed"

        # -----> Mã xác thực không đúng
        CODE_VERIFY_IS_INCORRECT = "9993"
        CODE_VERIFY_IS_INCORRECT_MESSAGE = 'Code verify is incorrect'

        # -----> Không có dữ liệu hoặc không còn dữ liệu
        NO_DATA_OR_END_OF_LIST_DATA = "9994"
        NO_DATA_OR_END_OF_LIST_DATA_MESSAGE = "No Data or end of list data"

        # ----> Không có người dùng này
        USER_IS_NOT_VALIDATED = "9995"
        USER_IS_NOT_VALIDATED_MESSAGE = "User is not validated"

        # ----> Người dùng đã tồn tại
        USER_EXISTED = "9996"
        USER_EXISTED_MESSAGE = "User existed."

        # ----> Phương thức này không đúng
        METHOD_IS_INVALID = "9997"
        METHOD_IS_INVALID_MESSAGE = "Method is invalid"

        # ---> Sai token
        TOKEN_IS_INVALID = "9998"
        TOKEN_IS_INVALID_MESSAGE = "Token is invalid."

        # ----> Lỗi exception
        EXCEPTION_ERROR = "9999"
        EXCEPTION_ERROR_MESSAGE = "Exception error."

        # ----> Lỗi mất kết nối hoặc thực thi câu SQL
        CANNOT_CONNECT_TO_DB = "1001"
        CANNOT_CONNECT_TO_DB_MESSAGE = "Can not connect to DB."

        # ----> Số lượng paramater không đầy đủ
        PARAMETER_IS_NOT_ENOUGH = "1002"
        PARAMETER_IS_NOT_ENOUGH_MESSAGE = "Parameter is not enought."

        # ----> Kiểu tham số không đúng đắn
        PARAMETER_TYPE_IS_INVALID = "1003"
        PARAMETER_TYPE_IS_INVALID_MESSAGE = "Parameter type is invalid."

        # ----> Giá trị của tham số không hợp lệ
        PARAMETER_VALUE_IS_INVALID = "1004"
        PARAMETER_VALUE_IS_INVALID_MESSAGE = "Parameter value is invalid."

        # ----> Unknow error
        UNKNOW_ERROR = "1005"
        UNKNOW_ERROR_MESSAGE = "Unknown error."

        # ----> Cỡ file vượt quá phép cho mức
        FILE_SIZE_IS_TOO_BIG = "1006"
        FILE_SIZE_IS_TOO_BIG_MESSAGE = "File size is too big."

        # ----> upload thất bại
        UPLOAD_FILE_FAILED = "1007"
        UPLOAD_FILE_FAILED_MESSAGE = "Upload File Failed!."

        # ----> Số lượng imgae vượt quá quy định
        MAXIMUM_NUMBER_OF_IMAGES = "1008"
        MAXIMUM_NUMBER_OF_IMAGES_MESSAGE = "Maximum number of images."

        # ----> Không có quyền truy cập tài nguyên
        NOT_ACCESS = "1009"
        NOT_ACCESS_MESSAGE = "Not access."

        # ----> Hành động này đã được người dùng thực hiện trước đây
        ACTION_HAS_BEEN_PREVIOUSLY_BY_THIS_USER = "1010"
        ACTION_HAS_BEEN_PREVIOUSLY_BY_THIS_USER_MESSAGE = "ation has been previously by this user."




