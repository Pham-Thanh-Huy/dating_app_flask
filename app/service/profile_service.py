import logging, os, base64
import uuid
from datetime import datetime
from flask import request
from marshmallow import ValidationError
from app.models import Profile
from app.schema.create.create_profile_schema import CreateProfileSchema
from app.schema.update.update_image_profile_schema import UpdateImageProfileSchema
from app.schema.update.update_profile_schema import UpdateProfileSchema
from app.utils.constant import Constant
from app.utils.response_util import internal_server_error_response
from app import db
from app.models import User


def create_profile_service():
    try:
        data = request.json
        schema = CreateProfileSchema()
        schema.load(data)

        user_id = data.get("user_id")
        profile = db.session.query(Profile).filter_by(user_id=user_id).first()

        if profile:
            return {
                "message": f"Đã tồn tại profile có user_id là {user_id}",
                "code": 400
            }

        user = db.session.query(User).filter_by(id=user_id).first()
        if not user:
            return {
                "message": f"Không tồn tại user với id là {user_id}",
                "code": 400
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
        db.session.commit()

        return {
            "profile": profile.to_dict(),
            "message": "Thêm profile thành công",
            "code": 200
        }
    except ValidationError as e:
        return {
            "message": e.messages,
            "code": Constant.API_STATUS.BAD_REQUEST
        }
    except Exception as e:
        logging.error(f"[ERROR-TO-CREATE-PROFILE] {e}")
        return internal_server_error_response()


def update_profile_service():
    try:
        data = request.get_json()
        schema = UpdateProfileSchema()
        schema.load(data)

        user_id = data.get("user_id")
        profile = db.session.query(Profile).filter_by(user_id=user_id).first()

        if not profile:
            return {
                "message": f"Không tồn tại profile có user_id là {user_id}",
                "code": Constant.API_STATUS.BAD_REQUEST
            }

        update_fields = [
            "name", "email", "avatar_url", "bio", "age", "gender", "location",
            "interests"
        ]

        for field in update_fields:
            if field in data:
                setattr(profile, field, data.get(field))

        db.session.commit()

        return {
            "profile": profile.to_dict(),
            "message": "update profile thành công",
            "code": 200
        }
    except ValidationError as e:
        return {
            "message": e.messages,
            "code": Constant.API_STATUS.BAD_REQUEST
        }
    except Exception as e:
        logging.error(f"[ERROR-TO-UPDATE-PROFILE] {e}")
        return internal_server_error_response()


def get_profile_by_user_id_service(user_id):
    try:
        profile = db.session.query(Profile).filter_by(user_id=user_id).first()
        if not profile:
            return {
                "message": f"Không tồn tại profile có user_id là {user_id}",
                "code": Constant.API_STATUS.BAD_REQUEST
            }

        return {
            "profile": profile.to_dict(),
            "message": Constant.API_STATUS.SUCCESS_MESSAGE,
            "code": Constant.API_STATUS.SUCCESS
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
                "message": f"Không tồn tại profile có user_id là {user_id}",
                "code": Constant.API_STATUS.BAD_REQUEST
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
        print(base64_image)

        return {
            "image": {
                "id": new_file_name,
                "image": base64_image
            },
            "message": Constant.API_STATUS.SUCCESS_MESSAGE,
            "code": Constant.API_STATUS.SUCCESS
        }
    except ValidationError as e:
        return {
            "message": e.messages,
            "code": Constant.API_STATUS.BAD_REQUEST
        }
    except Exception as e:
        logging.error(f"[ERROR-TO-GET-PROFILE-BY-ID] {e}")
        return internal_server_error_response()