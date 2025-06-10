import datetime
import logging, bcrypt
import time

from flask import request
from marshmallow import ValidationError
from app import db
from app.models import User
from app.schema.register_login_schema import RegisterLoginSchema
from app.schema.user_update_password_schema import UserUpdatePasswordSchema
from app.security.jwt_generation import generation_token
from app.utils.constant import Constant
from app.utils.response_util import internal_server_error_response
from app.utils.validate_util import parse_validation_error


def register_service():
    try:
        data = request.get_json(silent=True)
        if data is None:
            return {
                "message": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH_MESSAGE,
                "http_status_code": "400",
                "code": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH
            }

        # ----> Validate
        schema = RegisterLoginSchema()
        schema.load(data)

        username = data['username']
        password = data['password']

        user = db.session.query(User).filter_by(username=username).first()

        if user:
            return {
                "message": Constant.API_STATUS.USER_EXISTED_MESSAGE,
                "http_status_code": "400",
                "code": Constant.API_STATUS.USER_EXISTED
            }

        # HASH PASSWORD BCRYPT
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()  # ----> GEN SALT ($2a..., etc..)
        password = bcrypt.hashpw(password_bytes, salt)

        new_user = User(
            username=username,
            password=password,
            created_at=datetime.datetime.now()
        )

        # ------> SAVE TO DATABASE
        db.session.add(new_user)
        db.session.commit()

        return {
            "username": new_user.username,
            "message": Constant.API_STATUS.OK_MESSAGE,
            "http_status_code": Constant.API_STATUS.SUCCESS,
            "code": Constant.API_STATUS.OK,
            "created_at": new_user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
    except ValidationError as e:
        error_dict = parse_validation_error(e)
        return error_dict
    except Exception as e:
        logging.error(f"[ERROR-TO-REGISTER] {e}")
        return internal_server_error_response()

def login_service():
    try:
        # -----> GET DATA AND VALIDATE
        data = request.get_json(silent=True)

        if data is None:
            return {
                "message": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH_MESSAGE,
                "http_status_code": "400",
                "code": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH
            }

        schema = RegisterLoginSchema()
        schema.load(data)

        username = data['username']
        password = data['password']

        user_by_username = db.session.query(User).filter_by(username=username).first()

        user_or_password_incorrect_response = {
            "message": Constant.API_STATUS.USER_IS_NOT_VALIDATED_MESSAGE,
            "http_status_code": Constant.API_STATUS.BAD_REQUEST,
            "code": Constant.API_STATUS.USER_IS_NOT_VALIDATED
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
            "expired_date": exp.strftime('%Y-%m-%d %H:%M:%S'),
            "http_status_code": Constant.API_STATUS.SUCCESS,
            "message": Constant.API_STATUS.OK_MESSAGE,
            "code": Constant.API_STATUS.OK
        }
    except ValidationError as e:
        error_dict = parse_validation_error(e)
        return error_dict
    except Exception as e:
        logging.error(f"[ERROR-TO-LOGIN] {e}")
        return internal_server_error_response()

def reset_password_service():
    try:
        data = request.get_json(silent=True)
        if data is None:
            return {
                "message": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH_MESSAGE,
                "http_status_code": "400",
                "code": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH
            }
        schema = UserUpdatePasswordSchema()
        schema.load(data)

        user_by_id = db.session.query(User).filter_by(id=data['user_id']).first()
        if not user_by_id:
            return {
                "message": Constant.API_STATUS.USER_IS_NOT_VALIDATED_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.USER_IS_NOT_VALIDATED
            }

        old_password = data['old_password']
        new_password = data['new_password']

        # CHECK OLD_PASSWORD OTHER NEW_PASSWORD
        if old_password == new_password:
            return {
                "message": Constant.API_STATUS.PARAMETER_VALUE_IS_INVALID_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.PARAMETER_VALUE_IS_INVALID
            }

        # -----> CHECK OLD_PASSWORD - CURRENT PASSWORD IN DB
        old_password_bytes = old_password.encode("utf-8")
        password_check_bytes = user_by_id.password.encode("utf-8")

        password_check = bcrypt.checkpw(old_password_bytes, password_check_bytes)
        if not password_check:
            return {
                "message": Constant.API_STATUS.PARAMETER_VALUE_IS_INVALID_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.PARAMETER_VALUE_IS_INVALID
            }

        # -----> UPDATE PASSWORD
        password_bytes = new_password.encode("utf-8")
        salt = bcrypt.gensalt()  # Tạo salt
        hashed_password = bcrypt.hashpw(password_bytes, salt)

        user_by_id.password = hashed_password
        db.session.add(user_by_id)
        db.session.commit()

        return {
            "message": Constant.API_STATUS.OK_MESSAGE,
            "http_status_code": Constant.API_STATUS.SUCCESS,
            "code": Constant.API_STATUS.OK
        }
    except ValidationError as e:
        error_dict = parse_validation_error(e)
        return error_dict
    except Exception as e:
        logging.error(f"[ERROR-TO-DELETE-ACCOUNT] {e}")
        return internal_server_error_response()
