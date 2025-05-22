import logging, datetime
from tabnanny import check

from marshmallow import ValidationError
from sqlalchemy import text

from app import db
from flask import request
from app.schema.create.add_interaction_schema import AddInteractionSchema
from app.utils.constant import Constant
from app.utils.response_util import internal_server_error_response
from app.models import User, Profile, Interaction


def add_interaction_service():
    try:
        data = request.get_json()
        schema = AddInteractionSchema()
        schema.load(data)

        user_id = data.get("user_id")
        profile_id = data.get("profile_id")
        is_like = data.get("is_like")

        # ----> USER INTERACTION STANDARD
        user = db.session.query(User).filter_by(id=user_id).first()
        if not user:
            return {
                "message": f"Không tồn tại user user_id là `{user_id}` chuẩn bị tuơng tác!",
                "code": Constant.API_STATUS.BAD_REQUEST
            }

        # ---> GET PROFILE HAS BEEN INTERACTION BY USER
        profile = db.session.query(Profile).filter_by(id=profile_id).first()
        if not profile:
            return {
                "message": f"Không tồn tại profile có profile_id là `{profile_id}` sẽ dđưọc tương tác bởi user!",
                "code": Constant.API_STATUS.BAD_REQUEST
            }

        # CHECK USER_ID IN PROFILE = ID in user ----> CANCEL BECAUSE CANNOT INTERACTION WITH YOURSELF
        if profile.user_id == user.id:
            return {
                "message": f"Bạn Không thể tự tương tác với chính tài khoản của bạn!",
                "code": Constant.API_STATUS.BAD_REQUEST
            }

        # PROCESSING INTERACTION
        interaction = db.session.query(Interaction).filter_by(user_id=user_id, profile_id=profile_id).first()
        if interaction:
            interaction.is_like=is_like
        else:
            interaction = Interaction(
                is_like=is_like,
                user_id=user_id,
                profile_id=profile_id,
                created_at=datetime.datetime.now()
            )
        db.session.add(interaction)
        db.session.commit()

        # CHECK USER IN PROFILE interaction BY THE CURRENT USER HAVE INTERACTION BACK
        # ----> GET PROFILE BY CURRENT_USER INTERACTION
        check_interaction = False

        profile_by_current_user = db.session.query(Profile).filter_by(user_id=user.id).first()
        if profile_by_current_user:
            interaction_back = db.session.execute(
                text("SELECT * FROM interaction WHERE user_id=:profile_user_id AND profile_id=:user_profile_id"), {
                    "profile_user_id": profile.user_id, "user_profile_id": profile_by_current_user.id}).first()

            if interaction_back and interaction.is_like == interaction_back.is_like:
                check_interaction = True

        return {
            "code": Constant.API_STATUS.SUCCESS,
            "message": "Tương tác thành công",
            "is_match": 'True' if check_interaction == True else 'False',
            "interaction": {
                "user_id": user_id,
                "profile_id": profile_id,
                "is_like": 'True' if interaction.is_like == 1 else 'False',
                "created_at": interaction.created_at
            }
        }
    except ValidationError as e:
        return {
            "message": e.messages,
            "code": Constant.API_STATUS.BAD_REQUEST
        }
    except Exception as e:
        logging.error(f"[ERROR-TO-ADD-INTERACTION] {e}")
        return internal_server_error_response()
