import datetime
import logging

from flask import request
from marshmallow import ValidationError
from sqlalchemy.sql.operators import or_, and_
from app import db
from app.models import User, Conversation, Message
from app.schema.SendMessageSchema import SendMessageSchema
from app.schema.unmatch_schema import UnmatchSchema
from app.utils.constant import Constant
from app.utils.db_util import delete_list
from app.utils.response_util import internal_server_error_response
from app.utils.validate_util import parse_validation_error


def get_conversation_by_id_service(user_id: int):
    try:
        user = db.session.query(User).filter_by(id=user_id).first()
        if not user:
            return {
                "message": Constant.API_STATUS.USER_IS_NOT_VALIDATED_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.USER_IS_NOT_VALIDATED
            }

        # CREATE response
        response = []

        # GET CONVERSATION BY USER
        conversation_list = db.session.query(Conversation).filter(
            or_(
                Conversation.user_one_id == user.id,
                Conversation.user_two_id == user.id
            )
        ).all()

        if not conversation_list:
            return {
                "message": Constant.API_STATUS.NO_DATA_OR_END_OF_LIST_DATA_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.NO_DATA_OR_END_OF_LIST_DATA
            }

        # GET LAST MESSAGE
        for conversation in conversation_list:
            last_message = db.session.query(Message).filter_by(sender_id=user.id,
                                                               conversation_id=conversation.id).order_by(
                Message.created_at.desc()).first()
            response.append(
                {
                    "conversation": conversation.to_dict(),
                    "last_message": last_message.content if last_message else Constant.API_STATUS.NO_DATA_OR_END_OF_LIST_DATA_MESSAGE
                }
            )
        return {
            "chat": response,
            "code": Constant.API_STATUS.OK,
            "http_status_code": Constant.API_STATUS.SUCCESS,
            "message": Constant.API_STATUS.OK_MESSAGE
        }
    except Exception as e:
        logging.error(f"[ERROR-TO-GET-CONVERSATION-BY-ID] {e}")
        return internal_server_error_response()


def send_message_service():
    try:
        data = request.get_json(silent=True)
        if data is None:
            return {
                "message": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH_MESSAGE,
                "http_status_code": "400",
                "code": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH
            }
        schema = SendMessageSchema()
        schema.load(data)

        sender_id = data['sender']
        reveive_id = data['reveive']
        content = data['content']

        sender = db.session.query(User).filter_by(id=sender_id).first()
        if not sender:
            return {
                "message": Constant.API_STATUS.USER_IS_NOT_VALIDATED_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.USER_IS_NOT_VALIDATED
            }

        reveive = db.session.query(User).filter_by(id=reveive_id).first()
        if not reveive:
            return {
                "message": Constant.API_STATUS.USER_IS_NOT_VALIDATED_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.USER_IS_NOT_VALIDATED
            }

        # -----> IF CONVERSATION EXIT -> USE / IF NOT EXIT -> CREATE NEW CONVERSATION
        conversation = db.session.query(Conversation).filter(
            or_(
                and_(
                    Conversation.user_one_id == sender.id,
                    Conversation.user_two_id == reveive.id
                ),
                and_(
                    Conversation.user_one_id == reveive.id,
                    Conversation.user_two_id == sender.id
                )
            )
        ).first()

        if not conversation:
            conversation = Conversation(
                user_one_id=sender.id,
                user_two_id=reveive.id,
                created_at=datetime.datetime.now()
            )
            db.session.add(conversation)
            db.session.commit()

        # CHAT PROCESS
        chat = Message(
            sender_id=sender.id,
            conversation_id=conversation.id,
            content=content,
            created_at=datetime.datetime.now()
        )
        db.session.add(chat)
        db.session.commit()

        # ----> GET LIST MESSAGE IN CONVERSATION ORDER BY DESC
        message_list = db.session.query(Message).filter_by(conversation_id=conversation.id).order_by(
            Message.created_at.desc()).all()

        conversations = [{
            "sender": message.sender_id,
            "reveive": sender.id if message.sender_id != sender.id else reveive.id,
            "message": message.content,
            "latest_time": message.created_at,
            "id_conversation": conversation.id
        } for message in message_list]

        return {
            "code": Constant.API_STATUS.OK,
            "http_status_code": Constant.API_STATUS.SUCCESS,
            "message": Constant.API_STATUS.OK_MESSAGE,
            "conversations": conversations
        }
    except ValidationError as e:
        error_dict = parse_validation_error(e)
        return error_dict
    except Exception as e:
        logging.error(f"[ERROR-TO-SEND-MESSAGE] {e}")
        return internal_server_error_response()


def get_list_message_by_user_id_service(conversation_id: int, user_id: int):
    try:
        user = db.session.query(User).filter_by(id=user_id).first()
        if not user:
            return {
                "message": Constant.API_STATUS.USER_IS_NOT_VALIDATED_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.USER_IS_NOT_VALIDATED
            }

        conversation_not_found_response = {
            "message": Constant.API_STATUS.NO_DATA_OR_END_OF_LIST_DATA_MESSAGE,
            "http_status_code": Constant.API_STATUS.BAD_REQUEST,
            "code": Constant.API_STATUS.NO_DATA_OR_END_OF_LIST_DATA
        }
        conversation = db.session.query(Conversation).filter_by(id=conversation_id).first()
        if not conversation:
            return conversation_not_found_response

        # ----> GET LIST MESSAGE
        messages = db.session.query(Message).filter_by(conversation_id=conversation_id, sender_id=user_id).order_by(
            Message.created_at.desc()).all()
        if not messages:
            return conversation_not_found_response

        response = [{
            "id": message.id,
            "content": message.content,
            "sender_id": message.sender_id
        }
            for message in messages]

        return {
            "data": response,
            "http_status_code": Constant.API_STATUS.SUCCESS,
            "code": Constant.API_STATUS.OK,
            "message": Constant.API_STATUS.OK_MESSAGE,
        }
    except Exception as e:
        logging.error(f"[ERROR-TO-GET-LIST-MESSAGE-BY-USER-ID] {e}")
        return internal_server_error_response()


# ---> DELETE CONVERSATION
def unmatch_user_service():
    try:
        data = request.get_json(silent=True)
        if data is None:
            return {
                "message": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH_MESSAGE,
                "http_status_code": "400",
                "code": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH
            }
        schema = UnmatchSchema()
        schema.load(data)

        user_id = data['user_id']
        conversation_id = data['conversation_id']

        user = db.session.query(User).filter_by(id=user_id).first()
        if not user:
            return dict(message=Constant.API_STATUS.USER_IS_NOT_VALIDATED_MESSAGE,
                        http_status_code=Constant.API_STATUS.BAD_REQUEST,
                        code=Constant.API_STATUS.USER_IS_NOT_VALIDATED)

        conversation_not_found_response = {
            "message": Constant.API_STATUS.NO_DATA_OR_END_OF_LIST_DATA_MESSAGE,
            "http_status_code": Constant.API_STATUS.BAD_REQUEST,
            "code": Constant.API_STATUS.NO_DATA_OR_END_OF_LIST_DATA
        }
        conversation = db.session.query(Conversation).filter_by(id=conversation_id).first()
        if not conversation:
            return conversation_not_found_response

        # -----> CHECK EXIST CONVERSATION ID WITH USER_ID
        conversation = db.session.query(Conversation).filter(
            and_(
                Conversation.id == conversation_id,
                or_(
                    Conversation.user_one_id == user_id,
                    Conversation.user_two_id == user_id
                )
            )
        ).first()

        if not conversation:
            return {
                "message": Constant.API_STATUS.NO_DATA_OR_END_OF_LIST_DATA_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.NO_DATA_OR_END_OF_LIST_DATA
            }

        # -----> IF EXIST CONVERSATION ID WITH USER_ID
        message_list = db.session.query(Message).filter_by(conversation_id=conversation.id).all()
        delete_list(message_list)
        db.session.delete(conversation)
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
        logging.error(f"[ERROR-TO-GET-LIST-MESSAGE-BY-USER-ID] {e}")
        return internal_server_error_response()
