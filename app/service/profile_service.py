import logging, os, base64
import uuid
from datetime import datetime
from flask import request
from marshmallow import ValidationError
from app.models import Profile, Location
from app.schema.create.create_profile_schema import CreateProfileSchema
from app.schema.update.update_image_profile_schema import UpdateImageProfileSchema
from app.schema.update.update_profile_schema import UpdateProfileSchema
from app.utils.constant import Constant
from app.utils.request_other_api import get_lat_lng_by_address
from app.utils.response_util import internal_server_error_response
from app import db
from app.models import User
from app.utils.validate_util import parse_validation_error


def create_profile_service():
    try:
        data = request.get_json(silent=True)
        if data is None:
            return {
                "message": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH_MESSAGE,
                "http_status_code": "400",
                "code": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH
            }
        schema = CreateProfileSchema()
        schema.load(data)

        user_id = data.get("user_id")
        profile = db.session.query(Profile).filter_by(user_id=user_id).first()

        if profile:
            return {
                "message": Constant.API_STATUS.USER_EXISTED_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.USER_EXISTED
            }

        user = db.session.query(User).filter_by(id=user_id).first()
        if not user:
            return {
                "message": Constant.API_STATUS.USER_IS_NOT_VALIDATED_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.USER_IS_NOT_VALIDATED
            }
        profile = Profile(
            name=data.get("name"),
            email=data.get("email"),
            avatar_url=data.get("avatar_url"),
            bio=data.get("bio"),
            age=data.get("age"),
            gender=data.get("gender"),
            location=data.get("location", None),
            user_id=user_id,
            interests=data.get("interests", []),
            created_at=datetime.now()
        )

        db.session.add(profile)
        db.session.flush()

        # ----> UPDATE LOCATION
        result = get_lat_lng_by_address(data.get("location"))
        if result is not None:
            lat, lng = result
            location_rela = Location(
                lat=lat,
                lng=lng,
                profile_id=profile.id,
            )
            db.session.add(location_rela)
        db.session.commit()


        return {
            "profile": profile.to_dict(),
            "message": Constant.API_STATUS.OK_MESSAGE,
            "http_status_code": Constant.API_STATUS.SUCCESS,
            "code": Constant.API_STATUS.OK
        }
    except ValidationError as e:
        error_dict = parse_validation_error(e)
        return error_dict
    except Exception as e:
        logging.error(f"[ERROR-TO-CREATE-PROFILE] {e}")
        return internal_server_error_response()


def update_profile_service():
    try:
        data = request.get_json(silent=True)
        if data is None:
            return {
                "message": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH_MESSAGE,
                "http_status_code": "400",
                "code": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH
            }
        schema = UpdateProfileSchema()
        schema.load(data)

        user_id = data.get("user_id")
        profile = db.session.query(Profile).filter_by(user_id=user_id).first()

        if not profile:
            return {
                "message": Constant.API_STATUS.USER_IS_NOT_VALIDATED_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.USER_IS_NOT_VALIDATED
            }

        update_fields = [
            "name", "email", "avatar_url", "bio", "age", "gender", "location",
            "interests"
        ]

        for field in update_fields:
            if field in data:
                if field == "location":
                    result = get_lat_lng_by_address(data.get("location"))
                    if result is not None:
                        lat, lng = result

                        existing_location = db.session.query(Location).filter_by(profile_id=profile.id).first()

                        if existing_location:
                            existing_location.lat = lat
                            existing_location.lng = lng
                        else:
                            location_rela = Location(
                                lat=lat,
                                lng=lng,
                                profile_id=profile.id,
                            )
                            db.session.add(location_rela)

                    profile.location = data.get("location")

                else:
                    setattr(profile, field, data.get(field))

        db.session.commit()

        return {
            "profile": profile.to_dict(),
            "http_status_code": Constant.API_STATUS.SUCCESS,
            "message": Constant.API_STATUS.OK_MESSAGE,
            "code": Constant.API_STATUS.OK
        }
    except ValidationError as e:
        error_dict = parse_validation_error(e)
        return error_dict
    except Exception as e:
        logging.error(f"[ERROR-TO-UPDATE-PROFILE] {e}")
        return internal_server_error_response()


def get_profile_by_user_id_service(user_id):
    try:
        profile = db.session.query(Profile).filter_by(user_id=user_id).first()
        if not profile:
            return {
                "message": Constant.API_STATUS.USER_IS_NOT_VALIDATED_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.USER_IS_NOT_VALIDATED
            }

        return {
            "profile": profile.to_dict(),
            "http_status_code": Constant.API_STATUS.SUCCESS,
            "message": Constant.API_STATUS.OK_MESSAGE,
            "code": Constant.API_STATUS.OK
        }
    except Exception as e:
        logging.error(f"[ERROR-TO-GET-PROFILE-BY-ID] {e}")
        return internal_server_error_response()


def update_image_profile_service():
    try:
        user_id = request.form.get("user_id")
        image = request.files.get("image")

        data = {
            "user_id": user_id,
            "image": image
        }
        schema = UpdateImageProfileSchema()
        schema.load(data)

        profile = db.session.query(Profile).filter_by(user_id=user_id).first()
        if not profile:
            return {
                "message": Constant.API_STATUS.USER_IS_NOT_VALIDATED_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.USER_IS_NOT_VALIDATED
            }

        # PROCESSING IMAGE
        name, extension = os.path.splitext(image.filename)
        new_file_name = uuid.uuid4().__str__() + extension

        upload_dir = os.path.join('files', 'images', new_file_name)
        image.save(upload_dir)
        image.seek(0)  # -----> POINTER TO FIRST PLACE BECAUSE AFTER SAVE FILE POINTER IS LAST PLACE

        # CONVERT TO BASE 64
        image_bytes = image.read()
        base64_image = base64.b64encode(image_bytes).decode('utf-8')

        return {
            "image": {
                "id": new_file_name,
                "image": base64_image
            },
            "message": Constant.API_STATUS.OK_MESSAGE,
            "http_status_code": Constant.API_STATUS.SUCCESS,
            "code": Constant.API_STATUS.OK
        }
    except ValidationError as e:
       error_dict = parse_validation_error(e)
       return error_dict
    except Exception as e:
        logging.error(f"[ERROR-TO-GET-PROFILE-BY-ID] {e}")
        return internal_server_error_response()
