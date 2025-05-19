import datetime, logging, bcrypt
from flask import request
from marshmallow import ValidationError
from app import db
from app.models import User
from app.schema.register_login_schema import RegisterLoginSchema
from app.schema.user_update_password_schema import UserUpdatePasswordSchema
from app.security.jwt_generation import generation_token
from app.utils.constant import Constant
from app.utils.response_util import internal_server_error_response


def register_service():
    try:
        data = request.get_json()

        # ----> Validate
        schema = RegisterLoginSchema()
        schema.load(data)


        username = data['username']
        password = data['password']

        user = db.session.query(User).filter_by(username=username).first()

        if user:
            return {
                "message": f"Tên đăng nhập `{username}` đã tồn tại!",
                "code": Constant.API_STATUS.BAD_REQUEST
            }

        # HASH PASSWORD BCRYPT
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()  # ----> GEN SALT ($2a..., etc..)
        password = bcrypt.hashpw(password_bytes, salt)

        new_user = User(
            username=username,
            password=password,
            created_at=datetime.datetime.now(),
        )

        # ------> SAVE TO DATABASE
        db.session.add(new_user)
        db.session.commit()

        return {
            "username": new_user.username,
            "message": Constant.ADD_USER_SUCCESS,
            "code": Constant.API_STATUS.SUCCESS,
            "created_at": new_user.created_at,
        }
    except ValidationError as e:
        return {
            "message": e.messages,
            "code": Constant.API_STATUS.BAD_REQUEST
        }
    except Exception as e:
        logging.error(f"[ERROR-TO-REGISTER] {e}")
        return internal_server_error_response()

def login_service():
    try:
        #-----> GET DATA AND VALIDATE
        data = request.get_json()
        schema = RegisterLoginSchema()
        schema.load(data)

        username = data['username']
        password = data['password']

        user_by_username = db.session.query(User).filter_by(username=username).first()

        user_or_password_incorrect_response = {
            "message": Constant.USERNAME_OR_PASSWORD_INCORRECT,
            "code": Constant.API_STATUS.NOT_FOUND
        }
        if not user_by_username:
            return user_or_password_incorrect_response

        password_bytes = password.encode("utf-8")
        password_check_bytes = user_by_username.password.encode("utf-8")

        password_check = bcrypt.checkpw(password_bytes, password_check_bytes)

        if not password_check:
            return user_or_password_incorrect_response

        token, exp = generation_token(user_by_username.username)

        return {
            "token": token,
            "expired_date": exp,
            "message": Constant.LOGIN_SUCCESS,
            "code": Constant.API_STATUS.SUCCESS
        }
    except ValidationError as e:
        return {
            "message": e.messages,
            "code": Constant.API_STATUS.BAD_REQUEST
        }
    except Exception as e:
        logging.error(f"[ERROR-TO-LOGIN] {e}")
        return internal_server_error_response()



def reset_password_service():
    try:
        data = request.get_json()
        schema = UserUpdatePasswordSchema()
        schema.load(data)

        user_by_id = db.session.query(User).filter_by(id=data['user_id']).first()
        if not user_by_id:
            return {
                "message": f"Không tồn tại user với id là {data['user_id']}",
                "code": Constant.API_STATUS.NOT_FOUND
            }

        old_password = data['old_password']
        new_password = data['new_password']

        # CHECK OLD_PASSWORD OTHER NEW_PASSWORD
        if old_password == new_password:
            return {
                "message": f"Mật khẩu hiện cũ không được trùng với mật khẩu mới!",
                "code": Constant.API_STATUS.BAD_REQUEST
            }

        # -----> CHECK OLD_PASSWORD - CURRENT PASSWORD IN DB
        old_password_bytes = old_password.encode("utf-8")
        password_check_bytes = user_by_id.password.encode("utf-8")

        password_check = bcrypt.checkpw(old_password_bytes, password_check_bytes)
        if not password_check:
            return {
                "message": f"Mật khẩu hiện cũ không khớp với tài khoản này vui lòng nhập đúng mật khẩu!",
                "code": Constant.API_STATUS.BAD_REQUEST
            }

        # -----> UPDATE PASSWORD
        password_bytes = new_password.encode("utf-8")
        salt = bcrypt.gensalt()  # Tạo salt
        hashed_password = bcrypt.hashpw(password_bytes, salt)

        user_by_id.password = hashed_password
        db.session.add(user_by_id)
        db.session.commit()

        return {
            "message": Constant.CHANGE_PASSWORD_SUCCESS,
            "code": Constant.API_STATUS.SUCCESS
        }
    except ValidationError as e:
        return {
            "message": e.messages,
            "code": Constant.API_STATUS.BAD_REQUEST
        }
    except Exception as e:
        logging.error(f"[ERROR-TO-DELETE-ACCOUNT] {e}")
        return internal_server_error_response()
