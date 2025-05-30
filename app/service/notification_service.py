import logging

from app import db
from app.models import Notification
from app.utils.constant import Constant
from app.utils.response_util import internal_server_error_response


def get_notification_service(user_id: int, index: int, count: int):
    try:
        nofitication_list = db.session.query(Notification).filter_by(user_id=user_id).offset(index).limit(count).all()

        if not nofitication_list:
            return dict(message=f"user có id là {user_id} không có thông báo nào!",
                        code=Constant.API_STATUS.BAD_REQUEST)

        # MAP TO DICT
        notification_list_to_dict = [notification.to_dict() for notification in nofitication_list]
        return {
            "code": Constant.API_STATUS.SUCCESS,
            "message": Constant.API_STATUS.SUCCESS_MESSAGE,
            "profiles": notification_list_to_dict
        }
    except Exception as e:
        logging.error(f"[ERROR-TO-GET-NOTIFICATION] {e}")
        return internal_server_error_response()


def delete_notification_service(id: int):
    try:
        nofitication = db.session.query(Notification).filter_by(id=id).first()

        if not nofitication:
            return dict(message=f"không có thông báo nào với id là {id}!",
                        code=Constant.API_STATUS.BAD_REQUEST)

        db.session.delete(nofitication)
        db.session.commit()
        return {
            "message": "Xoá thông báo thành công",
            "code": Constant.API_STATUS.SUCCESS
        }
    except Exception as e:
        logging.error(f"[ERROR-TO-DELETE-NOTIFICATION] {e}")
        return internal_server_error_response()
