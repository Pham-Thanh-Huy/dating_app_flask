import logging
from datetime import datetime

from flask import request
from marshmallow import ValidationError
from app.models import Profile
from app.schema.create_profile_schema import CreateProfileSchema
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
        user = db.session.get(User).filter_by(user_id=user_id)
        if not user:
            return {
                "message": f"Không tồn tại user với id là {user_id}",
                "code": 400
            }
        profile = Profile(
            name = data.get("name"),
            email = data.get("email"),
            avatar_url = data.get("avatar_url"),
            bio = data.get("bio"),
            age = data.get("age"),
            gender = data.get("gender"),
            location = data.get("location", None),
            interests = data.get("interests", []),
            created_at=datetime.now()
        )

        db.session.add(profile)
        db.session.commit()

        return {
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
