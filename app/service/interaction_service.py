import logging, datetime
from marshmallow import ValidationError
from sqlalchemy import text
from app import db
from flask import request
from app.schema.create.add_interaction_schema import AddInteractionSchema
from app.schema.update.update_profile_schema import UpdateProfileSchema
from app.utils.constant import Constant
from app.utils.response_util import internal_server_error_response
from app.models import User, Profile, Interaction
from app.utils.validate_util import parse_validation_error


def add_interaction_service():
    try:
        data = request.get_json(silent=True)

        if not data:
            return {
                "code": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH,
                "message": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST
            }
        schema = AddInteractionSchema()
        schema.load(data)

        user_id = data.get("user_id")
        profile_id = data.get("profile_id")
        is_like = data.get("is_like")

        # ----> USER INTERACTION STANDARD
        user = db.session.query(User).filter_by(id=user_id).first()
        if not user:
            return {
                "message": Constant.API_STATUS.USER_IS_NOT_VALIDATED_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.USER_IS_NOT_VALIDATED
            }

        # ---> GET PROFILE HAS BEEN INTERACTION BY USER
        profile = db.session.query(Profile).filter_by(id=profile_id).first()
        if not profile:
            return {
                "message": Constant.API_STATUS.USER_IS_NOT_VALIDATED_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.USER_IS_NOT_VALIDATED
            }

        # CHECK USER_ID IN PROFILE = ID in user ----> CANCEL BECAUSE CANNOT INTERACTION WITH YOURSELF
        if profile.user_id == user.id:
            return {
                "message": Constant.API_STATUS.USER_EXISTED_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.USER_EXISTED
            }

        # PROCESSING INTERACTION
        interaction = db.session.query(Interaction).filter_by(user_id=user_id, profile_id=profile_id).first()
        if interaction:
            interaction.is_like = is_like
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
            "code": Constant.API_STATUS.OK,
            "http_status_code": Constant.API_STATUS.SUCCESS,
            "message": Constant.API_STATUS.OK_MESSAGE,
            "is_match": 'True' if check_interaction == True else 'False',
            "interaction": {
                "user_id": user_id,
                "profile_id": profile_id,
                "is_like": 'True' if interaction.is_like == 1 else 'False',
                "created_at": interaction.created_at
            }
        }
    except ValidationError as e:
        error_dict = parse_validation_error(e)
        return error_dict
    except Exception as e:
        logging.error(f"[ERROR-TO-ADD-INTERACTION] {e}")
        return internal_server_error_response()


def get_list_interaction_by_user_service(user_id: int, is_like: bool):
    try:
        user = db.session.query(User).filter_by(id=user_id).first()
        schema = UpdateProfileSchema(many=True)
        if not user:
            return {"message": Constant.API_STATUS.USER_IS_NOT_VALIDATED_MESSAGE,
                    "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                    "code": Constant.API_STATUS.USER_IS_NOT_VALIDATED}

        # ---> GET LIST INTERACTION BY USER
        interaction_list = db.session.query(Interaction).filter_by(user_id=user_id, is_like=is_like).all()
        if not interaction_list:
            return {
                "message": Constant.API_STATUS.NO_DATA_OR_END_OF_LIST_DATA_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.NO_DATA_OR_END_OF_LIST_DATA}

        profile_list = [db.session.query(Profile).filter_by(id=interaction.profile_id).first() for interaction in
                        interaction_list]
        profile_list_map_to_dict = [profile.to_dict() for profile in profile_list]

        return {
            "is_like": is_like,
            "profile": profile_list_map_to_dict,
            "message": Constant.API_STATUS.OK_MESSAGE,
            "http_status_code": Constant.API_STATUS.SUCCESS,
            "code": Constant.API_STATUS.OK
        }
    except Exception as e:
        logging.error(f"[ERROR-TO-GET-LIST-INTERACTION-BY-USER] {e}")
        return internal_server_error_response()
