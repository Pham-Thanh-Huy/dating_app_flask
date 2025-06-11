import logging

from app import db
from app.models import Notification
from app.utils.constant import Constant
from app.utils.response_util import internal_server_error_response


def get_notification_service(user_id: int, index: int, count: int):
    try:
        nofitication_list = db.session.query(Notification).filter_by(user_id=user_id).offset(index).limit(count).all()

        if not nofitication_list:
            return {
                "message": Constant.API_STATUS.NO_DATA_OR_END_OF_LIST_DATA_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.NO_DATA_OR_END_OF_LIST_DATA
            }

        # MAP TO DICT
        notification_list_to_dict = [notification.to_dict() for notification in nofitication_list]
        return {
            "code": Constant.API_STATUS.OK,
            "http_status_code": Constant.API_STATUS.SUCCESS,
            "message": Constant.API_STATUS.OK_MESSAGE,
            "profiles": notification_list_to_dict
        }
    except Exception as e:
        logging.error(f"[ERROR-TO-GET-NOTIFICATION] {e}")
        return internal_server_error_response()


def delete_notification_service(id: int):
    try:
        nofitication = db.session.query(Notification).filter_by(id=id).first()

        if not nofitication:
            return{
                "message": Constant.API_STATUS.NO_DATA_OR_END_OF_LIST_DATA_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.NO_DATA_OR_END_OF_LIST_DATA
            }


        db.session.delete(nofitication)
        db.session.commit()
        return {
            "code": Constant.API_STATUS.OK,
            "http_status_code": Constant.API_STATUS.SUCCESS,
            "message": Constant.API_STATUS.OK_MESSAGE,
        }
    except Exception as e:
        logging.error(f"[ERROR-TO-DELETE-NOTIFICATION] {e}")
        return internal_server_error_response()
