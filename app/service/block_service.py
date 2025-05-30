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


def block_user_service():
    try:
        data = request.get_json()
        block_user_id = data.get('block_user_id') if data else None

        if not block_user_id:
            return dict(message="Block_user_id không đưọc dể trống", code=Constant.API_STATUS.BAD_REQUEST)

        user_is_blocked = db.session.query(User).filter_by(id=block_user_id).first()
        if not user_is_blocked:
            return dict(message=f"Không tồn tại user(sắp bị block) có ID là `{block_user_id}`!",
                        code=Constant.API_STATUS.BAD_REQUEST)

        # PARSE TOKEN TO USERNAME AND GET USER BY USERNAME AND BLOCK USER_iD
        data, err = parse_token_get_username(request.headers.get('Authorization', '')[len('Bearer '):].strip())

        if err:
            return dict(message=data, code=Constant.API_STATUS.INTERNAL_SERVER_ERROR)

        user = db.session.query(User).filter_by(username=data).first()

        if user.id == user_is_blocked.id:
            return {
                "message": "Bạn không thể tự block chính mình",
                "code": Constant.API_STATUS.BAD_REQUEST
            }

        block = Block(user_id=user.id, block_user_id=user_is_blocked.id, created_at=datetime.datetime.now())
        db.session.add(block)
        db.session.commit()

        return {
            "code": Constant.API_STATUS.SUCCESS,
            "message": "Block thành công"
        }
    except Exception as e:
        logging.error(f"[ERROR-TO-BLOCK-USER] {e}")
        return internal_server_error_response()


def get_list_block_service():
    try:
        data = request.get_json()
        schema = GetListBlockSchema()
        schema.load(data)

        user_id = data.get('user_id')
        index = data.get('index')
        count = data.get('count')

        user = db.session.query(User).filter_by(id=user_id).first()
        if not user:
            return dict(message=f"Không tồn tại user có ID là `{user_id}`!", code=Constant.API_STATUS.BAD_REQUEST)

        block_list = db.session.query(Block).filter_by(user_id=user.id).offset(index).limit(count).all()

        user_is_blocked_list = [db.session.query(User).filter_by(id=block.block_user_id).first() for block in
                                block_list]

        profile_by_user_blocked_list = [db.session.query(Profile).filter_by(user_id=u.id).first() for u in
                                        user_is_blocked_list]

        profile_blocked_to_dict = [profile.to_dict() for profile in profile_by_user_blocked_list]

        return {
            "message": Constant.API_STATUS.SUCCESS_MESSAGE,
            "code": Constant.API_STATUS.SUCCESS,
            "profiles": profile_blocked_to_dict
        }
    except ValidationError as e:
        return {
            "message": e.messages,
            "code": Constant.API_STATUS.BAD_REQUEST
        }
    except Exception as e:
        logging.error(f"[ERROR-TO-BLOCK-USER] {e}")
        return internal_server_error_response()


def unblock_user_service(block_user_id: int):
    try:
        data, err = parse_token_get_username(request.headers.get('Authorization', '')[len('Bearer '):].strip())

        if err:
            return dict(message=data, code=Constant.API_STATUS.INTERNAL_SERVER_ERROR)

        user = db.session.query(User).filter_by(username=data).first()

        user_is_blocked = db.session.query(User).filter_by(id=block_user_id).first()
        if not user_is_blocked:
            return dict(message=f"Không tồn tại user bị block có ID là `{block_user_id}`!", code=Constant.API_STATUS.BAD_REQUEST)

        if user.id == user_is_blocked.id:
            return {
                "message": "Bạn không thể hủy block chính mình",
                "code": Constant.API_STATUS.BAD_REQUEST
            }

        block = db.session.query(Block).filter_by(user_id=user.id, block_user_id=block_user_id).first()

        if not block:
            return dict(message=f"user {user.username} không block user có id là {user_is_blocked.id}",
                        code=Constant.API_STATUS.BAD_REQUEST)

        db.session.delete(block)
        db.session.commit()
        return {
            "code": Constant.API_STATUS.SUCCESS,
            "message": "Bỏ block thành công"
        }
    except Exception as e:
        logging.error(f"[ERROR-TO-UNBLOCK-USER] {e}")
        return internal_server_error_response()
