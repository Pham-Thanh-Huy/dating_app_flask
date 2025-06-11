import datetime
import logging

from flask import request
from marshmallow import ValidationError

from app import db
from app.models import Block, User, Profile
from app.schema.block_schema import GetListBlockSchema
from app.security.jwt_generation import parse_token_get_username
from app.utils.constant import Constant
from app.utils.response_util import internal_server_error_response
from app.utils.validate_util import parse_validation_error


def block_user_service():
    try:
        data = request.get_json(silent=True)
        if data is None:
            return {
                "message": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH_MESSAGE,
                "http_status_code": "400",
                "code": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH
            }
        block_user_id = data.get('block_user_id') if data else None

        if not block_user_id:
            return {
                "message": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH_MESSAGE,
                "http_status_code": "400",
                "code": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH
            }

        user_is_blocked = db.session.query(User).filter_by(id=block_user_id).first()
        if not user_is_blocked:
            return {
                "message": Constant.API_STATUS.USER_IS_NOT_VALIDATED_MESSAGE,
                "http_status_code": "400",
                "code": Constant.API_STATUS.USER_IS_NOT_VALIDATED
            }

        # PARSE TOKEN TO USERNAME AND GET USER BY USERNAME AND BLOCK USER_iD
        data, err = parse_token_get_username(request.headers.get('Authorization', '')[len('Bearer '):].strip())

        if err:
            return internal_server_error_response()

        user = db.session.query(User).filter_by(username=data).first()

        if user.id == user_is_blocked.id:
            return {
                "message": Constant.API_STATUS.NO_DATA_OR_END_OF_LIST_DATA_MESSAGE,
                "http_status_code": "400",
                "code": Constant.API_STATUS.NO_DATA_OR_END_OF_LIST_DATA
            }

        block = Block(user_id=user.id, block_user_id=user_is_blocked.id, created_at=datetime.datetime.now())
        db.session.add(block)
        db.session.commit()

        return {
            "code": Constant.API_STATUS.OK,
            "http_status_code": Constant.API_STATUS.SUCCESS,
            "message": Constant.API_STATUS.OK_MESSAGE
        }
    except Exception as e:
        logging.error(f"[ERROR-TO-BLOCK-USER] {e}")
        return internal_server_error_response()


def get_list_block_service():
    try:
        data = request.get_json(silent=True)
        if not data:
            return {
                "message": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH
            }
        schema = GetListBlockSchema()
        schema.load(data)

        user_id = data.get('user_id')
        index = data.get('index')
        count = data.get('count')

        user = db.session.query(User).filter_by(id=user_id).first()
        if not user:
            return dict(message=Constant.API_STATUS.USER_IS_NOT_VALIDATED_MESSAGE,
                        http_status_code=Constant.API_STATUS.BAD_REQUEST,
                        code=Constant.API_STATUS.USER_IS_NOT_VALIDATED)

        block_list = db.session.query(Block).filter_by(user_id=user.id).offset(index).limit(count).all()

        user_is_blocked_list = [db.session.query(User).filter_by(id=block.block_user_id).first() for block in
                                block_list]

        profile_by_user_blocked_list = [db.session.query(Profile).filter_by(user_id=u.id).first() for u in
                                        user_is_blocked_list]

        profile_blocked_to_dict = [profile.to_dict() for profile in profile_by_user_blocked_list]

        return {
            "message": Constant.API_STATUS.OK_MESSAGE,
            "http_status_code": Constant.API_STATUS.SUCCESS,
            "code": Constant.API_STATUS.OK,
            "profiles": profile_blocked_to_dict
        }
    except ValidationError as e:
        error_dict = parse_validation_error(e)
        return error_dict
    except Exception as e:
        logging.error(f"[ERROR-TO-BLOCK-USER] {e}")
        return internal_server_error_response()


def unblock_user_service(block_user_id: int):
    try:
        data, err = parse_token_get_username(request.headers.get('Authorization', '')[len('Bearer '):].strip())

        if err:
            logging.error("PARSE TOKEN TO USER NOT SUCCESS -> INTERNAL SERVER ERRIR")
            return internal_server_error_response()

        user = db.session.query(User).filter_by(username=data).first()

        user_is_blocked = db.session.query(User).filter_by(id=block_user_id).first()
        if not user_is_blocked:
            return {
                "message": Constant.API_STATUS.USER_IS_NOT_VALIDATED_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.USER_IS_NOT_VALIDATED
            }

        if user.id == user_is_blocked.id:
            return {
                "message": Constant.API_STATUS.NO_DATA_OR_END_OF_LIST_DATA_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.NO_DATA_OR_END_OF_LIST_DATA
            }
        block = db.session.query(Block).filter_by(user_id=user.id, block_user_id=block_user_id).first()

        if not block:
            return  {
                "message": Constant.API_STATUS.NO_DATA_OR_END_OF_LIST_DATA_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.NO_DATA_OR_END_OF_LIST_DATA
            }

        db.session.delete(block)
        db.session.commit()
        return {
            "message": Constant.API_STATUS.OK_MESSAGE,
            "http_status_code": Constant.API_STATUS.SUCCESS,
            "code": Constant.API_STATUS.OK,
        }
    except Exception as e:
        logging.error(f"[ERROR-TO-UNBLOCK-USER] {e}")
        return internal_server_error_response()
