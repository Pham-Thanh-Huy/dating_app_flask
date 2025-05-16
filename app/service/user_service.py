import logging
from app import db
from app.models import User
from app.utils.constant import Constant

def delete_account_service(user_id: int):
    try:
        user = db.session.query(User).filter_by(id=user_id).first()

        if not user:
            return {
                "message": f"Không tồn tại user với id là {user_id}",
                "code": Constant.API_STATUS.NOT_FOUND
            }

        db.session.delete(user)
        db.session.commit()

        return {
            "message": f"Người dùng có (id: {user_id}) {Constant.DELETE_SUCCESS}",
            "code": Constant.API_STATUS.SUCCESS
        }
    except Exception as e:
        logging.error(f"[ERROR-TO-DELETE-ACCOUNT] {e}")
        return {
            "message": Constant.API_STATUS.INTERNAL_SERVER_ERROR_MESSAGE,
            "code": Constant.API_STATUS.INTERNAL_SERVER_ERROR
        }