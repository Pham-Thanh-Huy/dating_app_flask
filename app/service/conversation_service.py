import logging

from sqlalchemy.sql.operators import or_

from app import db
from app.models import User, Conversation, Message
from app.utils.constant import Constant
from app.utils.response_util import internal_server_error_response


def get_conversation_by_id_service(user_id: int):
    try:
        user = db.session.query(User).filter_by(id=user_id).first()
        if not user:
            return {
                "message": f"Không tồn tại user user_id là `{user_id}`!",
                "code": Constant.API_STATUS.BAD_REQUEST
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
                "message": f"user_id `{user_id} chưa có bất kì 1 đoạn hội thoại nào`",
                "code": Constant.API_STATUS.BAD_REQUEST
            }

        # GET LAST MESSAGE
        for conversation in conversation_list:
            last_message = db.session.query(Message).filter_by(sender_id=user.id,
                                                               conversation_id=conversation.id).order_by(
                Message.created_at.desc()).first()
            response.append(
                {
                    "conversation": conversation.to_dict(),
                    "last_message": last_message.content if last_message else f"Không có tin nhắn nào vì user có id là `{user_id}` chưa nhắn"
                }
            )
        return {
            "chat": response,
            "code": Constant.API_STATUS.SUCCESS,
            "message": Constant.API_STATUS.SUCCESS_MESSAGE
        }
    except Exception as e:
        logging.error(f"[ERROR-TO-GET-CONVERSATION-BY-ID] {e}")
        return internal_server_error_response()


# def