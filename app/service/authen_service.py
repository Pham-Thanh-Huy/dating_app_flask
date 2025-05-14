import datetime, logging, bcrypt
from flask import request
from marshmallow import ValidationError
from app import db
from app.models import User
from app.schema.register_login_schema import RegisterLoginSchema
from app.utils.constant import Constant


def register_service():
    try:
        data = request.get_json()
        # ----> Validate
        try:
            schema = RegisterLoginSchema()
            schema.load(data)
        except ValidationError as e:
            return {
                "message": e.messages,
                "code": Constant.API_STATUS.BAD_REQUEST
            }

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
    except Exception as e:
        logging.error(f"[ERROR-TO-REGISTER] {e}")
        return {
            "message": Constant.API_STATUS.INTERNAL_SERVER_ERROR_MESSAGE,
            "code": Constant.API_STATUS.INTERNAL_SERVER_ERROR
        }


def login_service():
    try:
        data = request.get_json()
        try:
            schema = RegisterLoginSchema()
            schema.load(data)
        except ValidationError as e:
            return {
                "message": e.messages,
                "code": Constant.API_STATUS.BAD_REQUEST
            }

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
        password_check = bcrypt.checkpw(password_bytes, user_by_username.password)

        if not password_check:
            return user_or_password_incorrect_response



        return None
    except Exception as e:
        logging.error(f"[ERROR-TO-LOGIN] {e}")
        return {
            "message": Constant.API_STATUS.INTERNAL_SERVER_ERROR_MESSAGE,
            "code": Constant.API_STATUS.INTERNAL_SERVER_ERROR
        }
