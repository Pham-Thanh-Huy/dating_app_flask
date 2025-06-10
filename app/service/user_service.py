import logging
from app import db
from app.models import User
from app.utils.constant import Constant
from app.utils.response_util import internal_server_error_response


def delete_account_service(user_id: int):
    try:
        user = db.session.query(User).filter_by(id=user_id).first()

        if not user:
            return {
                "message": Constant.API_STATUS.USER_IS_NOT_VALIDATED_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.USER_IS_NOT_VALIDATED
            }

        db.session.delete(user)
        db.session.commit()

        return {
            "message": Constant.API_STATUS.OK_MESSAGE,
            "http_status_code": Constant.API_STATUS.SUCCESS,
            "code": Constant.API_STATUS.OK
        }
    except Exception as e:
        logging.error(f"[ERROR-TO-DELETE-ACCOUNT] {e}")
        return internal_server_error_response()